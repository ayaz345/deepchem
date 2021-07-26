import math
import numpy as np
try:
  import torch
  import torch.nn as nn
  import torch.nn.functional as F
except:
  raise ImportError('These classes require Torch to be installed.')


class ScaleNorm(nn.Module):
  """Apply Scale Normalization to input.

  The ScaleNorm layer first computes the square root of the scale, then computes the matrix/vector norm of the input tensor.
  The norm value is calculated as `sqrt(scale) / matrix norm`.
  Finally, the result is returned as `input_tensor * norm value`.

  This layer can be used instead of LayerNorm when a scaled version of the norm is required.
  Instead of performing the scaling operation (`scale / norm`) in a lambda-like layer, we are defining it within this layer to make prototyping more efficient.

  References
  ----------
  .. [1] Lukasz Maziarka et al. "Molecule Attention Transformer" Graph Representation Learning workshop and Machine Learning and the Physical Sciences workshop at NeurIPS 2019. 2020. https://arxiv.org/abs/2002.08264

  Examples
  --------
  >>> import deepchem as dc
  >>> scale = 0.35
  >>> layer = dc.models.torch_models.layers.ScaleNorm(scale)
<<<<<<< HEAD
  >>> input_tensor = torch.tensor([[1.269, 39.36], [0.00918, -9.12]])
=======
  >>> input_tensor = torch.Tensor([[1.269, 39.36], [0.00918, -9.12]])
>>>>>>> Added encoder layers
  >>> output_tensor = layer(input_tensor)
  """

  def __init__(self, scale: float, eps: float = 1e-5):
    """Initialize a ScaleNorm layer.

    Parameters
    ----------
    scale: float
      Scale magnitude.
    eps: float
      Epsilon value. Default = 1e-5.
    """

    super(ScaleNorm, self).__init__()
    self.scale = nn.Parameter(torch.tensor(math.sqrt(scale)))
    self.eps = eps

  def forward(self, x: torch.Tensor):
    norm = self.scale / torch.norm(x, dim=-1, keepdim=True).clamp(min=self.eps)
    return x * norm


<<<<<<< HEAD
class MultiHeadedMATAttention(nn.Module):
  """First constructs an attention layer tailored to the Molecular Attention Transformer [1]_ and then converts it into Multi-Headed Attention.

  In Multi-Headed attention the attention mechanism multiple times parallely through the multiple attention heads.
  Thus, different subsequences of a given sequences can be processed differently.
  The query, key and value parameters are split multiple ways and each split is passed separately through a different attention head.
  References
  ----------
  .. [1] Lukasz Maziarka et al. "Molecule Attention Transformer" Graph Representation Learning workshop and Machine Learning and the Physical Sciences workshop at NeurIPS 2019. 2020. https://arxiv.org/abs/2002.08264
  Examples
  --------
  >>> import deepchem as dc
  >>> from rdkit import Chem
  >>> mol = Chem.MolFromSmiles("CC")
  >>> adj_matrix = Chem.GetAdjacencyMatrix(mol)
  >>> distance_matrix = Chem.GetDistanceMatrix(mol)
  >>> import deepchem.models.torch_models.layers
  >>> layer = dc.models.torch_models.layers.MultiHeadedMATAttention(dist_kernel='softmax', lambda_attention=0.33, lambda_distance=0.33, h=2, hsize=2, dropout_p=0.0)
  >>> input_tensor = torch.tensor([[1., 2.], [5., 6.]])
  >>> mask = torch.tensor([[1., 1.], [1., 1.]])
  >>> result = layer(input_tensor, input_tensor, input_tensor, mask, 0.0, adj_matrix, distance_matrix)
  """

  def __init__(self,
               dist_kernel: str,
               lambda_attention: float,
               lambda_distance: float,
               h: int,
               hsize: int,
               dropout_p: float,
               output_bias: bool = True):
    """Initialize a multi-headed attention layer.
    Parameters
    ----------
    dist_kernel: str
      Kernel activation to be used. Can be either 'softmax' for softmax or 'exp' for exponential.
    lambda_attention: float
      Constant to be multiplied with the attention matrix.
    lambda_distance: float
      Constant to be multiplied with the distance matrix.
    h: int
      Number of attention heads.
    hsize: int
      Size of dense layer.
    dropout_p: float
      Dropout probability.
    output_bias: bool
      If True, dense layers will use bias vectors.
    """
    super().__init__()
    if dist_kernel == "softmax":
      self.dist_kernel = lambda x: torch.softmax(-x, dim=-1)
    elif dist_kernel == "exp":
      self.dist_kernel = lambda x: torch.exp(-x)
    self.lambda_attention = lambda_attention
    self.lambda_distance = lambda_distance
    self.lambda_adjacency = 1.0 - self.lambda_attention - self.lambda_distance
    self.d_k = hsize // h
    self.h = h
    linear_layer = nn.Linear(hsize, hsize)
    self.linear_layers = nn.ModuleList([linear_layer for _ in range(3)])
    self.dropout_p = nn.Dropout(dropout_p)
    self.output_linear = nn.Linear(hsize, hsize, output_bias)

  def _single_attention(self,
                        query: torch.Tensor,
                        key: torch.Tensor,
                        value: torch.Tensor,
                        mask: torch.Tensor,
                        dropout_p: float,
                        adj_matrix: np.ndarray,
                        distance_matrix: np.ndarray,
                        eps: float = 1e-6,
                        inf: float = 1e12):
    """Defining and computing output for a single MAT attention layer.
    Parameters
    ----------
    query: torch.Tensor
      Standard query parameter for attention.
    key: torch.Tensor
      Standard key parameter for attention.
    value: torch.Tensor
      Standard value parameter for attention.
    mask: torch.Tensor
      Masks out padding values so that they are not taken into account when computing the attention score.
    dropout_p: float
      Dropout probability.
    adj_matrix: np.ndarray
      Adjacency matrix of the input molecule, returned from dc.feat.MATFeaturizer()
    dist_matrix: np.ndarray
      Distance matrix of the input molecule, returned from dc.feat.MATFeaturizer()
    eps: float
      Epsilon value
    inf: float
      Value of infinity to be used.
    """
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)

    if mask is not None:
      scores = scores.masked_fill(
          mask.unsqueeze(1).repeat(1, query.shape[1], query.shape[2], 1) == 0,
          -inf)
    p_attn = F.softmax(scores, dim=-1)

    adj_matrix = adj_matrix / (
        torch.sum(torch.tensor(adj_matrix), dim=-1).unsqueeze(1) + eps)
    p_adj = adj_matrix.repeat(1, query.shape[1], 1, 1)

    distance_matrix = torch.tensor(distance_matrix).masked_fill(
        mask.repeat(1, mask.shape[-1], 1) == 0, np.inf)
    distance_matrix = self.dist_kernel(distance_matrix)
    p_dist = distance_matrix.unsqueeze(1).repeat(1, query.shape[1], 1, 1)
    p_weighted = self.lambda_attention * p_attn + self.lambda_distance * p_dist + self.lambda_adjacency * p_adj
    p_weighted = self.dropout_p(p_weighted)

    bd = value.broadcast_to(p_weighted.shape)
    return torch.matmul(p_weighted.float(), bd.float()), p_attn

  def forward(self,
              query: torch.Tensor,
              key: torch.Tensor,
              value: torch.Tensor,
              mask: torch.Tensor,
              dropout_p: float,
              adj_matrix: np.ndarray,
              distance_matrix: np.ndarray,
              eps: float = 1e-6,
              inf: float = 1e12):
    """Output computation for the MultiHeadedAttention layer.
    Parameters
    ----------
    query: torch.Tensor
      Standard query parameter for attention.
    key: torch.Tensor
      Standard key parameter for attention.
    value: torch.Tensor
      Standard value parameter for attention.
    mask: torch.Tensor
      Masks out padding values so that they are not taken into account when computing the attention score.
    """
    if mask is not None:
      mask = mask.unsqueeze(1)

    batch_size = query.size(0)

    query, key, value = [
        layer(x).view(batch_size, -1, self.h, self.d_k).transpose(1, 2)
        for layer, x in zip(self.linear_layers, (query, key, value))
    ]

    x, _ = self._single_attention(query, key, value, mask, dropout_p,
                                  adj_matrix, distance_matrix, eps, inf)
    x = x.transpose(1, 2).contiguous().view(batch_size, -1, self.h * self.d_k)

    return self.output_linear(x)
=======
class MATEncoder(nn.Module):
  """Encoder block for the Molecule Attention Transformer [1]_.

  A stack of N layers which form the MAT encoder block. The block primarily consists of a self-attention layer and a feed-forward layer.
  This block is constructed from its basic layer: MATEncoderLayer. See dc.models.torch_models.layers.MATEncoderLayer for more details regarding the working of the block.

  References
  ----------
  .. [1] Lukasz Maziarka et al. "Molecule Attention Transformer" Graph Representation Learning workshop and Machine Learning and the Physical Sciences workshop at NeurIPS 2019. 2020. https://arxiv.org/abs/2002.08264

  Examples
  --------
  >>> import deepchem as dc
  >>> block = dc.models.torch_models.layers.MATEncoder(dist_kernel = 'softmax', lambda_attention = 0.33, lambda_adistance = 0.33, h = 8, sa_hsize = 1024, sa_dropout_p = 0.1, d_input = 1024, activation = 'relu', n_layers = 1, ff_dropout_p = 0.1, encoder_hsize = 1024, encoder_dropout_p = 0.1, N = 3)
  """

  def __init__(self, dist_kernel, lambda_attention, lambda_distance, h,
               sa_hsize, sa_dropout_p, output_bias, d_input, d_hidden, d_output,
               activation, n_layers, ff_dropout_p, encoder_hsize,
               encoder_dropout_p, N):
    """Initialize a MATEncoder block.

    Parameters
    ----------
    Parameters
    ----------
    dist_kernel: str
      Kernel activation to be used. Can be either 'softmax' for softmax or 'exp' for exponential, for the self-attention layer.
    lambda_attention: float
      Constant to be multiplied with the attention matrix in the self-attention layer.
    lambda_distance: float
      Constant to be multiplied with the distance matrix in the self-attention layer.
    h: int
      Number of attention heads for the self-attention layer.
    sa_hsize: int
      Size of dense layer in the self-attention layer.
    sa_dropout_p: float
      Dropout probability for the self-attention layer.
    output_bias: bool
      If True, dense layers will use bias vectors in the self-attention layer.
    d_input: int
      Size of input layer in the feed-forward layer.
    d_hidden: int
      Size of hidden layer in the feed-forward layer.
    d_output: int
      Size of output layer in the feed-forward layer.
    activation: str
      Activation function to be used in the feed-forward layer.
      Can choose between 'relu' for ReLU, 'leakyrelu' for LeakyReLU, 'prelu' for PReLU,
      'tanh' for TanH, 'selu' for SELU, 'elu' for ELU and 'linear' for linear activation.
    n_layers: int
      Number of layers in the feed-forward layer.
    dropout_p: float
      Dropout probability in the feeed-forward layer.
    encoder_hsize: int
      Size of Dense layer for the encoder itself.
    encoder_dropout_p: float
      Dropout probability for connections in the encoder layer.
    N: int
      Number of identical encoder layers to be stacked.
    """

    super(MATEncoder, self).__init__()
    encoder_layer = MATEncoderLayer(
        dist_kernel, lambda_attention, lambda_distance, h, sa_hsize,
        sa_dropout_p, output_bias, d_input, d_hidden, d_output, activation,
        n_layers, ff_dropout_p, encoder_hsize, encoder_dropout_p)
    self.layers = nn.ModuleList([encoder_layer for _ in range(N)])
    self.norm = nn.LayerNorm(encoder_layer.size)

  def forward(self, x, mask, **kwargs):
    """Output computation for the MATEncoder block.

    Parameters
    ----------
    x: torch.Tensor
      Input tensor.
    mask: torch.Tensor
      Mask for padding so that padded values do not get included in attention score calculation.
    """

    for layer in self.layers:
      x = layer(x, mask, **kwargs)
    return self.norm(x)


class MATEncoderLayer(nn.Module):
  """Encoder layer for use in the Molecular Attention Transformer [1]_.

  The MATEncoder layer is formed by adding self-attention and feed-forward to the encoder block.
  It is the basis of the MATEncoder block.

  References
  ----------
  .. [1] Lukasz Maziarka et al. "Molecule Attention Transformer" Graph Representation Learning workshop and Machine Learning and the Physical Sciences workshop at NeurIPS 2019. 2020. https://arxiv.org/abs/2002.08264

  Examples
  --------
  >>> import deepchem as dc
  >>> layer = dc.models.torch_models.layers.MATEncoderLayer(dist_kernel = 'softmax', lambda_attention = 0.33, lambda_distance = 0.33, h = 8, sa_hsize = 1024, sa_dropout_p = 0.1, d_input = 1024, activation = 'relu', n_layers = 1, ff_dropout_p = 0.1, encoder_hsize = 1024, encoder_dropout_p = 0.1)
  """

  def __init__(self, dist_kernel, lambda_attention, lambda_distance, h,
               sa_hsize, sa_dropout_p, output_bias, d_input, d_hidden, d_output,
               activation, n_layers, ff_dropout_p, encoder_hsize,
               encoder_dropout_p):
    """Initialize a MATEncoder layer.

    Parameters
    ----------
    dist_kernel: str
      Kernel activation to be used. Can be either 'softmax' for softmax or 'exp' for exponential, for the self-attention layer.
    lambda_attention: float
      Constant to be multiplied with the attention matrix in the self-attention layer.
    lambda_distance: float
      Constant to be multiplied with the distance matrix in the self-attention layer.
    h: int
      Number of attention heads for the self-attention layer.
    sa_hsize: int
      Size of dense layer in the self-attention layer.
    sa_dropout_p: float
      Dropout probability for the self-attention layer.
    output_bias: bool
      If True, dense layers will use bias vectors in the self-attention layer.
    d_input: int
      Size of input layer in the feed-forward layer.
    d_hidden: int
      Size of hidden layer in the feed-forward layer.
    d_output: int
      Size of output layer in the feed-forward layer.
    activation: str
      Activation function to be used in the feed-forward layer.
      Can choose between 'relu' for ReLU, 'leakyrelu' for LeakyReLU, 'prelu' for PReLU,
      'tanh' for TanH, 'selu' for SELU, 'elu' for ELU and 'linear' for linear activation.
    n_layers: int
      Number of layers in the feed-forward layer.
    dropout_p: float
      Dropout probability in the feeed-forward layer.
    encoder_hsize: int
      Size of Dense layer for the encoder itself.
    encoder_dropout_p: float
      Dropout probability for connections in the encoder layer.
    """

    super(MATEncoderLayer, self).__init__()
    self.self_attn = MultiHeadedMATAttention(dist_kernel, lambda_attention,
                                             lambda_distance, h, sa_hsize,
                                             sa_dropout_p, output_bias)
    self.feed_forward = PositionwiseFeedForward(
        d_input, d_hidden, d_output, activation, n_layers, ff_dropout_p)
    layer = SublayerConnection(size=encoder_hsize, dropout_p=encoder_dropout_p)
    self.sublayer = nn.ModuleList([layer for _ in range(2)])
    self.size = encoder_hsize

  def forward(self, x, mask, **kwargs):
    """Output computation for the MATEncoder layer.

    Parameters
    ----------
    x: torch.Tensor
      Input tensor.
    mask: torch.Tensor
      Masks out padding values so that they are not taken into account when computing the attention score.
    """
    x = self.sublayer[0](x,
                         lambda x: self.self_attn(x, x, x, mask=mask, **kwargs))
    return self.sublayer[1](x, self.feed_forward)


class SublayerConnection(nn.Module):
  """SublayerConnection layer which establishes a residual connection, as used in the Molecular Attention Transformer [1]_.

  The SublayerConnection layer is a residual layer which is then passed through Layer Normalization.
  The residual connection is established by computing the dropout-adjusted layer output of a normalized input tensor and adding this to the originial input tensor.

  References
  ----------
  .. [1] Lukasz Maziarka et al. "Molecule Attention Transformer" Graph Representation Learning workshop and Machine Learning and the Physical Sciences workshop at NeurIPS 2019. 2020. https://arxiv.org/abs/2002.08264

  Examples
  --------
  >>> import deepchem as dc
  >>> scale = 0.35
  >>> layer = dc.models.torch_models.layers.SublayerConnection(2, 0.)
  >>> output = layer(torch.Tensor([1.,2.]), nn.Linear(2,1))
  """

  def __init__(self, size, dropout_p):
    """Initialize a SublayerConnection Layer.

    Parameters
    ----------
    size: int
      Size of layer.
    dropout_p: float
      Dropout probability.
    """

    super(SublayerConnection, self).__init__()
    self.norm = nn.LayerNorm(size)
    self.dropout_p = nn.Dropout(dropout_p)

  def forward(self, x, sublayer):
    """Output computation for the SublayerConnection layer.

    Takes an input tensor x, then adds the dropout-adjusted sublayer output for normalized x to it.

    Parameters
    ----------
    x: torch.Tensor
      Input tensor.
    sublayer: nn.Module
      Layer whose output for normalized x will be added to x.
    """
    return x + self.dropout_p(sublayer(self.norm(x)))


class PositionwiseFeedForward(nn.Module):
  """PositionwiseFeedForward is a layer used to define the position-wise feed-forward (FFN) algorithm for the Molecular Attention Transformer [1]_

  Each layer in the MAT encoder contains a fully connected feed-forward network which applies two linear transformations and the given activation function.
  This is done in addition to the SublayerConnection module.

  References
  ----------
  .. [1] Lukasz Maziarka et al. "Molecule Attention Transformer" Graph Representation Learning workshop and Machine Learning and the Physical Sciences workshop at NeurIPS 2019. 2020. https://arxiv.org/abs/2002.08264

  Examples
  --------
  >>> import deepchem as dc
  >>> feed_fwd_layer = dc.models.torch_models.layers.PositionwiseFeedForward(d_input = 1024, d_hidden = None, d_output = None, activation = 'relu', n_layers = 1, dropout_p = 0.1)
  """

  def __init__(self,
               *,
               d_input,
               d_hidden=None,
               d_output=None,
               activation,
               n_layers,
               dropout_p):
    """Initialize a PositionwiseFeedForward layer.

    Parameters
    ----------
    d_input: int
      Size of input layer.
    d_hidden: int
      Size of hidden layer.
    d_output: int
      Size of output layer.
    activation: str
      Activation function to be used. Can choose between 'relu' for ReLU, 'leakyrelu' for LeakyReLU, 'prelu' for PReLU,
      'tanh' for TanH, 'selu' for SELU, 'elu' for ELU and 'linear' for linear activation.
    n_layers: int
      Number of layers.
    dropout_p: float
      Dropout probability.
    """

    super(PositionwiseFeedForward, self).__init__()

    if activation == 'relu':
      self.activation = nn.ReLU()

    elif activation == 'leakyrelu':
      self.activation = nn.LeakyReLU(0.1)

    elif activation == 'prelu':
      self.activation = nn.PReLU()

    elif activation == 'tanh':
      self.activation = nn.Tanh()

    elif activation == 'selu':
      self.activation = nn.SELU()

    elif activation == 'elu':
      self.activation = nn.ELU()

    elif activation == "linear":
      self.activation = lambda x: x

    self.n_layers = n_layers
    d_output = d_output if d_output is not None else d_input
    d_hidden = d_hidden if d_hidden is not None else d_input

    if n_layers == 1:
      self.linears = [nn.Linear(d_input, d_output)]

    else:
      self.linears = [nn.Linear(d_input, d_hidden)] + \
                      [nn.Linear(d_hidden, d_hidden) for _ in range(n_layers - 2)] + \
                      [nn.Linear(d_hidden, d_output)]

    self.linears = nn.ModuleList(self.linears)
    dropout_layer = nn.Dropout(dropout_p)
    self.dropout_p = nn.ModuleList([dropout_layer for _ in range(n_layers)])
    self.act_func = activation

  def forward(self, x):
    """Output Computation for the PositionwiseFeedForward layer.

    Parameters
    ----------
    x: torch.Tensor
      Input tensor.
    """

    if self.n_layers == 0:
      return x

    elif self.n_layers == 1:
      return self.dropout_p[0](self.act_func(self.linears[0](x)))

    else:
      for i in range(self.n_layers - 1):
        x = self.dropout_p[i](self.act_func(self.linears[i](x)))
      return self.linears[-1](x)
>>>>>>> Added encoder layers
