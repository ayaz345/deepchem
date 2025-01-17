import pandas as pd
import os
import pickle
import array
from bisect import bisect_left
import gzip
import time
import shutil
import deepchem
import requests
import argparse
import numpy as np

data_dir = deepchem.utils.get_data_dir()
sdf_dir = os.path.join(data_dir, "Data")


class PCBADatsetBuilder:

  def __init__(self):

    self.pcba_128_assay_list = "PCBA-1030,PCBA-1379,PCBA-1452,PCBA-1454,PCBA-1457,PCBA-1458,PCBA-1460,PCBA-1461,PCBA-1468,PCBA-1469,PCBA-1471,PCBA-1479,PCBA-1631,PCBA-1634,PCBA-1688,PCBA-1721,PCBA-2100,PCBA-2101,PCBA-2147,PCBA-2242,PCBA-2326,PCBA-2451,PCBA-2517,PCBA-2528,PCBA-2546,PCBA-2549,PCBA-2551,PCBA-2662,PCBA-2675,PCBA-2676,PCBA-411,PCBA-463254,PCBA-485281,PCBA-485290,PCBA-485294,PCBA-485297,PCBA-485313,PCBA-485314,PCBA-485341,PCBA-485349,PCBA-485353,PCBA-485360,PCBA-485364,PCBA-485367,PCBA-492947,PCBA-493208,PCBA-504327,PCBA-504332,PCBA-504333,PCBA-504339,PCBA-504444,PCBA-504466,PCBA-504467,PCBA-504706,PCBA-504842,PCBA-504845,PCBA-504847,PCBA-504891,PCBA-540276,PCBA-540317,PCBA-588342,PCBA-588453,PCBA-588456,PCBA-588579,PCBA-588590,PCBA-588591,PCBA-588795,PCBA-588855,PCBA-602179,PCBA-602233,PCBA-602310,PCBA-602313,PCBA-602332,PCBA-624170,PCBA-624171,PCBA-624173,PCBA-624202,PCBA-624246,PCBA-624287,PCBA-624288,PCBA-624291,PCBA-624296,PCBA-624297,PCBA-624417,PCBA-651635,PCBA-651644,PCBA-651768,PCBA-651965,PCBA-652025,PCBA-652104,PCBA-652105,PCBA-652106,PCBA-686970,PCBA-686978,PCBA-686979,PCBA-720504,PCBA-720532,PCBA-720542,PCBA-720551,PCBA-720553,PCBA-720579,PCBA-720580,PCBA-720707,PCBA-720708,PCBA-720709,PCBA-720711,PCBA-743255,PCBA-743266,PCBA-875,PCBA-881,PCBA-883,PCBA-884,PCBA-885,PCBA-887,PCBA-891,PCBA-899,PCBA-902,PCBA-903,PCBA-904,PCBA-912,PCBA-914,PCBA-915,PCBA-924,PCBA-925,PCBA-926,PCBA-927,PCBA-938,PCBA-995".split(
        ',')
    self.pcba_146_assay_list = "PCBA-1030,PCBA-1379,PCBA-1452,PCBA-1454,PCBA-1457,PCBA-1458,PCBA-1460,PCBA-1461,PCBA-1468,PCBA-1469,PCBA-1471,PCBA-1479,PCBA-1631,PCBA-1634,PCBA-1688,PCBA-1721,PCBA-2100,PCBA-2101,PCBA-2147,PCBA-2242,PCBA-2326,PCBA-2451,PCBA-2517,PCBA-2528,PCBA-2546,PCBA-2549,PCBA-2551,PCBA-2662,PCBA-2675,PCBA-2676,PCBA-411,PCBA-463254,PCBA-485281,PCBA-485290,PCBA-485294,PCBA-485297,PCBA-485313,PCBA-485314,PCBA-485341,PCBA-485349,PCBA-485353,PCBA-485360,PCBA-485364,PCBA-485367,PCBA-492947,PCBA-493208,PCBA-504327,PCBA-504332,PCBA-504333,PCBA-504339,PCBA-504444,PCBA-504466,PCBA-504467,PCBA-504706,PCBA-504842,PCBA-504845,PCBA-504847,PCBA-504891,PCBA-540276,PCBA-540317,PCBA-588342,PCBA-588453,PCBA-588456,PCBA-588579,PCBA-588590,PCBA-588591,PCBA-588795,PCBA-588855,PCBA-602179,PCBA-602233,PCBA-602310,PCBA-602313,PCBA-602332,PCBA-624170,PCBA-624171,PCBA-624173,PCBA-624202,PCBA-624246,PCBA-624287,PCBA-624288,PCBA-624291,PCBA-624296,PCBA-624297,PCBA-624417,PCBA-651635,PCBA-651644,PCBA-651768,PCBA-651965,PCBA-652025,PCBA-652104,PCBA-652105,PCBA-652106,PCBA-686970,PCBA-686978,PCBA-686979,PCBA-720504,PCBA-720532,PCBA-720542,PCBA-720551,PCBA-720553,PCBA-720579,PCBA-720580,PCBA-720707,PCBA-720708,PCBA-720709,PCBA-720711,PCBA-743255,PCBA-743266,PCBA-875,PCBA-881,PCBA-883,PCBA-884,PCBA-885,PCBA-887,PCBA-891,PCBA-899,PCBA-902,PCBA-903,PCBA-904,PCBA-912,PCBA-914,PCBA-915,PCBA-924,PCBA-925,PCBA-926,PCBA-927,PCBA-938,PCBA-995,PCBA-686971,PCBA-504834,PCBA-588856,PCBA-720533,PCBA-1865,PCBA-651820,PCBA-923,PCBA-493014,PCBA-504648,PCBA-624418,PCBA-1159614,PCBA-2289,PCBA-1159524,PCBA-1463,PCBA-504832,PCBA-540256,PCBA-485298,PCBA-2685".split(
        ',')
    self.pcba_2475_assay_list = "PCBA-1259344,PCBA-588834,PCBA-1159536,PCBA-1259321,PCBA-1259320,PCBA-1259256,PCBA-1259255,PCBA-1259253,PCBA-1259252,PCBA-1159605,PCBA-1159604,PCBA-1259244,PCBA-1259243,PCBA-1259242,PCBA-1259241,PCBA-720687,PCBA-720675,PCBA-720674,PCBA-1224890,PCBA-1224889,PCBA-1224888,PCBA-1224887,PCBA-1224886,PCBA-1224885,PCBA-1224884,PCBA-1224883,PCBA-1224882,PCBA-1224881,PCBA-1224880,PCBA-1224879,PCBA-1224878,PCBA-1224877,PCBA-1224876,PCBA-1224875,PCBA-1224874,PCBA-1224873,PCBA-1224872,PCBA-1224871,PCBA-1224870,PCBA-1224869,PCBA-1224868,PCBA-1224867,PCBA-1224862,PCBA-1224861,PCBA-1224860,PCBA-1224859,PCBA-1224858,PCBA-1224857,PCBA-1224856,PCBA-1224855,PCBA-1224854,PCBA-1224853,PCBA-1224863,PCBA-1224847,PCBA-1224846,PCBA-1224845,PCBA-1224844,PCBA-1224843,PCBA-1224839,PCBA-1224838,PCBA-1224837,PCBA-1224836,PCBA-1224835,PCBA-1224823,PCBA-1224822,PCBA-1224821,PCBA-1224820,PCBA-1224819,PCBA-1224818,PCBA-1159614,PCBA-1159513,PCBA-1159512,PCBA-1159511,PCBA-1159510,PCBA-1382,PCBA-1159577,PCBA-1159574,PCBA-1159573,PCBA-1159572,PCBA-1159571,PCBA-1159570,PCBA-1159569,PCBA-1159568,PCBA-1159567,PCBA-1159566,PCBA-1117284,PCBA-1159553,PCBA-1159552,PCBA-1159551,PCBA-1117274,PCBA-1117272,PCBA-1117271,PCBA-720691,PCBA-1053202,PCBA-1159529,PCBA-1159527,PCBA-1053204,PCBA-1053203,PCBA-1159526,PCBA-1159525,PCBA-1159524,PCBA-1117265,PCBA-1053181,PCBA-1159521,PCBA-1159520,PCBA-1053169,PCBA-1053167,PCBA-1159517,PCBA-1159516,PCBA-1159515,PCBA-1053141,PCBA-1053140,PCBA-1053134,PCBA-1053132,PCBA-1053121,PCBA-1053120,PCBA-977620,PCBA-977612,PCBA-977609,PCBA-977617,PCBA-977616,PCBA-977615,PCBA-743509,PCBA-743507,PCBA-743497,PCBA-743483,PCBA-743481,PCBA-743440,PCBA-743417,PCBA-743413,PCBA-743403,PCBA-743399,PCBA-743381,PCBA-743434,PCBA-743422,PCBA-743373,PCBA-1117362,PCBA-1117361,PCBA-1117358,PCBA-1117359,PCBA-743372,PCBA-743296,PCBA-743284,PCBA-743425,PCBA-743234,PCBA-743231,PCBA-743229,PCBA-743450,PCBA-743423,PCBA-743404,PCBA-743400,PCBA-743389,PCBA-743384,PCBA-743186,PCBA-743183,PCBA-743175,PCBA-743181,PCBA-743172,PCBA-743167,PCBA-1117295,PCBA-743154,PCBA-743153,PCBA-743125,PCBA-743124,PCBA-743408,PCBA-743360,PCBA-743357,PCBA-743316,PCBA-743312,PCBA-743311,PCBA-743308,PCBA-743307,PCBA-743305,PCBA-743304,PCBA-743303,PCBA-743302,PCBA-743298,PCBA-743159,PCBA-743131,PCBA-743129,PCBA-743128,PCBA-743123,PCBA-743095,PCBA-720728,PCBA-743115,PCBA-743111,PCBA-743104,PCBA-743102,PCBA-743097,PCBA-743068,PCBA-743062,PCBA-743022,PCBA-743026,PCBA-743016,PCBA-720715,PCBA-720714,PCBA-720696,PCBA-720695,PCBA-720673,PCBA-720672,PCBA-720671,PCBA-720651,PCBA-720649,PCBA-743195,PCBA-743187,PCBA-743179,PCBA-743178,PCBA-743171,PCBA-743170,PCBA-743161,PCBA-1117277,PCBA-743083,PCBA-720622,PCBA-743225,PCBA-743224,PCBA-743223,PCBA-743222,PCBA-743221,PCBA-743220,PCBA-743218,PCBA-743217,PCBA-743215,PCBA-743213,PCBA-743212,PCBA-743211,PCBA-743210,PCBA-743209,PCBA-743203,PCBA-743202,PCBA-743194,PCBA-743191,PCBA-743094,PCBA-743086,PCBA-743085,PCBA-743084,PCBA-743081,PCBA-720590,PCBA-743080,PCBA-743079,PCBA-743075,PCBA-743074,PCBA-743069,PCBA-743066,PCBA-743065,PCBA-743064,PCBA-743042,PCBA-743041,PCBA-743040,PCBA-743036,PCBA-743035,PCBA-743033,PCBA-743015,PCBA-743014,PCBA-743012,PCBA-720693,PCBA-720692,PCBA-720686,PCBA-720685,PCBA-720684,PCBA-720683,PCBA-720682,PCBA-720681,PCBA-720680,PCBA-720679,PCBA-720678,PCBA-720635,PCBA-720634,PCBA-651634,PCBA-651633,PCBA-651632,PCBA-651631,PCBA-743110,PCBA-743058,PCBA-743057,PCBA-743056,PCBA-743055,PCBA-1053205,PCBA-720595,PCBA-720593,PCBA-720568,PCBA-720567,PCBA-720562,PCBA-1053185,PCBA-1053184,PCBA-1053183,PCBA-1053174,PCBA-1053173,PCBA-651917,PCBA-651734,PCBA-624284,PCBA-624063,PCBA-602455,PCBA-602241,PCBA-624078,PCBA-1053144,PCBA-1053143,PCBA-743244,PCBA-743146,PCBA-743142,PCBA-1053127,PCBA-1053126,PCBA-1053125,PCBA-1053124,PCBA-1053122,PCBA-1053119,PCBA-1053118,PCBA-1053117,PCBA-1053115,PCBA-1035475,PCBA-686993,PCBA-743342,PCBA-977607,PCBA-977606,PCBA-977605,PCBA-686969,PCBA-686967,PCBA-686962,PCBA-686961,PCBA-623995,PCBA-743479,PCBA-743478,PCBA-743477,PCBA-743472,PCBA-743471,PCBA-743470,PCBA-743464,PCBA-743453,PCBA-743452,PCBA-743441,PCBA-743446,PCBA-743444,PCBA-743416,PCBA-743415,PCBA-743412,PCBA-743402,PCBA-743396,PCBA-743395,PCBA-743394,PCBA-686932,PCBA-686917,PCBA-686916,PCBA-686915,PCBA-652285,PCBA-652283,PCBA-652282,PCBA-652276,PCBA-743327,PCBA-743326,PCBA-743325,PCBA-652250,PCBA-652227,PCBA-743343,PCBA-743341,PCBA-743340,PCBA-743329,PCBA-652222,PCBA-652198,PCBA-652196,PCBA-743339,PCBA-652207,PCBA-743336,PCBA-652179,PCBA-652170,PCBA-652287,PCBA-652286,PCBA-652165,PCBA-652161,PCBA-743319,PCBA-743317,PCBA-743314,PCBA-652177,PCBA-652265,PCBA-652123,PCBA-652112,PCBA-743297,PCBA-743295,PCBA-743294,PCBA-743293,PCBA-743292,PCBA-743291,PCBA-743288,PCBA-2675,PCBA-743049,PCBA-652060,PCBA-652059,PCBA-720608,PCBA-720605,PCBA-720624,PCBA-720607,PCBA-720602,PCBA-720598,PCBA-743276,PCBA-743275,PCBA-743197,PCBA-743150,PCBA-743149,PCBA-743145,PCBA-743144,PCBA-743048,PCBA-743047,PCBA-743046,PCBA-743045,PCBA-743044,PCBA-743043,PCBA-743021,PCBA-743020,PCBA-519,PCBA-743267,PCBA-743266,PCBA-652173,PCBA-489002,PCBA-720701,PCBA-743262,PCBA-743260,PCBA-743259,PCBA-652172,PCBA-743255,PCBA-743254,PCBA-651977,PCBA-651976,PCBA-489003,PCBA-743245,PCBA-652046,PCBA-652043,PCBA-624288,PCBA-651913,PCBA-651912,PCBA-720726,PCBA-652289,PCBA-720727,PCBA-651875,PCBA-651872,PCBA-651855,PCBA-651853,PCBA-651849,PCBA-651842,PCBA-651874,PCBA-651862,PCBA-743059,PCBA-651790,PCBA-651788,PCBA-652183,PCBA-652180,PCBA-652175,PCBA-651775,PCBA-651920,PCBA-651996,PCBA-743019,PCBA-652164,PCBA-652140,PCBA-720729,PCBA-686933,PCBA-651753,PCBA-652211,PCBA-652194,PCBA-720724,PCBA-720711,PCBA-720709,PCBA-720708,PCBA-720707,PCBA-651760,PCBA-720697,PCBA-720690,PCBA-652077,PCBA-652034,PCBA-652033,PCBA-652032,PCBA-651676,PCBA-651670,PCBA-720659,PCBA-720653,PCBA-720652,PCBA-720650,PCBA-720646,PCBA-720645,PCBA-720512,PCBA-720636,PCBA-720632,PCBA-651947,PCBA-651605,PCBA-651642,PCBA-720597,PCBA-720591,PCBA-720589,PCBA-720588,PCBA-720587,PCBA-720586,PCBA-720584,PCBA-720579,PCBA-720580,PCBA-720578,PCBA-720577,PCBA-720576,PCBA-720575,PCBA-720573,PCBA-720572,PCBA-624496,PCBA-624495,PCBA-720569,PCBA-720537,PCBA-720570,PCBA-720564,PCBA-687026,PCBA-687023,PCBA-686931,PCBA-686930,PCBA-686929,PCBA-686928,PCBA-652239,PCBA-624500,PCBA-624460,PCBA-651841,PCBA-651816,PCBA-720565,PCBA-720553,PCBA-720551,PCBA-687040,PCBA-651837,PCBA-651836,PCBA-651809,PCBA-624473,PCBA-624458,PCBA-720548,PCBA-720542,PCBA-651835,PCBA-720538,PCBA-720534,PCBA-624439,PCBA-624425,PCBA-624410,PCBA-624409,PCBA-720541,PCBA-720540,PCBA-720536,PCBA-720535,PCBA-720533,PCBA-720532,PCBA-720528,PCBA-720527,PCBA-720526,PCBA-720525,PCBA-720524,PCBA-720523,PCBA-720522,PCBA-720519,PCBA-651840,PCBA-651839,PCBA-720518,PCBA-720517,PCBA-652280,PCBA-652275,PCBA-651863,PCBA-651829,PCBA-651807,PCBA-720514,PCBA-720513,PCBA-720498,PCBA-651854,PCBA-651845,PCBA-2517,PCBA-651878,PCBA-720507,PCBA-720506,PCBA-652019,PCBA-624373,PCBA-720504,PCBA-720503,PCBA-720502,PCBA-720501,PCBA-720500,PCBA-720499,PCBA-720497,PCBA-720496,PCBA-720495,PCBA-720494,PCBA-720493,PCBA-686947,PCBA-651795,PCBA-651773,PCBA-651772,PCBA-651771,PCBA-651770,PCBA-651591,PCBA-651588,PCBA-651586,PCBA-651585,PCBA-651584,PCBA-624492,PCBA-624490,PCBA-624489,PCBA-624488,PCBA-624440,PCBA-624430,PCBA-624429,PCBA-624428,PCBA-624427,PCBA-624426,PCBA-624364,PCBA-624368,PCBA-624366,PCBA-624363,PCBA-624362,PCBA-720491,PCBA-720490,PCBA-651577,PCBA-624324,PCBA-624316,PCBA-624315,PCBA-687032,PCBA-687031,PCBA-687030,PCBA-687029,PCBA-687028,PCBA-687027,PCBA-624299,PCBA-624290,PCBA-624289,PCBA-686948,PCBA-687022,PCBA-624275,PCBA-624270,PCBA-687020,PCBA-624259,PCBA-687017,PCBA-687013,PCBA-687005,PCBA-687004,PCBA-687003,PCBA-687002,PCBA-687001,PCBA-687000,PCBA-686999,PCBA-686998,PCBA-686997,PCBA-686994,PCBA-686991,PCBA-686985,PCBA-686984,PCBA-686980,PCBA-686979,PCBA-686978,PCBA-651752,PCBA-624376,PCBA-624375,PCBA-624374,PCBA-624372,PCBA-624369,PCBA-624367,PCBA-624365,PCBA-624361,PCBA-624360,PCBA-624359,PCBA-624391,PCBA-624389,PCBA-686971,PCBA-686970,PCBA-686960,PCBA-686959,PCBA-686957,PCBA-652193,PCBA-624205,PCBA-624177,PCBA-624176,PCBA-624175,PCBA-624164,PCBA-624163,PCBA-624174,PCBA-624075,PCBA-624074,PCBA-624073,PCBA-624072,PCBA-686920,PCBA-624107,PCBA-624106,PCBA-624105,PCBA-624104,PCBA-624056,PCBA-624055,PCBA-624049,PCBA-624048,PCBA-624047,PCBA-624046,PCBA-624045,PCBA-624034,PCBA-624027,PCBA-624020,PCBA-624018,PCBA-624016,PCBA-624014,PCBA-624012,PCBA-624011,PCBA-624023,PCBA-624019,PCBA-624006,PCBA-623998,PCBA-623993,PCBA-623991,PCBA-652252,PCBA-624094,PCBA-624093,PCBA-623985,PCBA-623981,PCBA-623969,PCBA-623965,PCBA-652244,PCBA-652242,PCBA-652241,PCBA-623973,PCBA-623972,PCBA-623970,PCBA-623966,PCBA-623951,PCBA-623950,PCBA-623912,PCBA-652208,PCBA-623945,PCBA-623938,PCBA-623904,PCBA-623903,PCBA-623899,PCBA-623897,PCBA-623894,PCBA-623887,PCBA-623885,PCBA-623881,PCBA-652156,PCBA-623883,PCBA-623876,PCBA-623873,PCBA-623864,PCBA-623863,PCBA-623875,PCBA-652145,PCBA-623934,PCBA-623930,PCBA-652135,PCBA-624029,PCBA-624024,PCBA-652128,PCBA-652127,PCBA-652121,PCBA-652116,PCBA-651579,PCBA-651563,PCBA-624474,PCBA-623895,PCBA-623880,PCBA-602414,PCBA-602408,PCBA-652106,PCBA-652105,PCBA-652104,PCBA-602394,PCBA-652102,PCBA-652101,PCBA-602391,PCBA-602373,PCBA-602371,PCBA-602370,PCBA-602366,PCBA-602362,PCBA-623947,PCBA-588775,PCBA-602308,PCBA-602306,PCBA-602285,PCBA-652062,PCBA-652058,PCBA-652057,PCBA-652053,PCBA-652047,PCBA-602269,PCBA-602268,PCBA-652042,PCBA-652041,PCBA-652040,PCBA-602407,PCBA-602316,PCBA-602309,PCBA-488949,PCBA-652025,PCBA-652016,PCBA-652015,PCBA-652023,PCBA-602288,PCBA-602258,PCBA-602256,PCBA-652006,PCBA-652005,PCBA-602317,PCBA-651989,PCBA-602242,PCBA-602190,PCBA-602189,PCBA-602187,PCBA-602186,PCBA-602185,PCBA-602184,PCBA-651971,PCBA-651970,PCBA-651968,PCBA-624162,PCBA-651967,PCBA-540355,PCBA-2769,PCBA-2768,PCBA-2756,PCBA-2755,PCBA-2754,PCBA-1926,PCBA-1919,PCBA-651965,PCBA-651713,PCBA-651712,PCBA-624479,PCBA-624476,PCBA-602227,PCBA-602225,PCBA-602223,PCBA-602222,PCBA-602221,PCBA-602220,PCBA-602219,PCBA-602218,PCBA-602216,PCBA-602214,PCBA-602165,PCBA-602164,PCBA-651956,PCBA-602161,PCBA-602160,PCBA-602158,PCBA-651939,PCBA-651937,PCBA-602129,PCBA-602121,PCBA-602126,PCBA-651848,PCBA-651823,PCBA-651595,PCBA-651593,PCBA-588842,PCBA-651745,PCBA-651675,PCBA-651820,PCBA-588828,PCBA-588826,PCBA-651818,PCBA-651817,PCBA-651815,PCBA-651814,PCBA-651813,PCBA-651812,PCBA-602310,PCBA-651804,PCBA-651802,PCBA-651793,PCBA-651791,PCBA-651789,PCBA-651784,PCBA-651768,PCBA-651778,PCBA-651777,PCBA-588810,PCBA-651758,PCBA-651757,PCBA-651755,PCBA-651754,PCBA-651751,PCBA-651749,PCBA-588771,PCBA-651743,PCBA-651741,PCBA-588776,PCBA-651700,PCBA-588777,PCBA-588754,PCBA-651720,PCBA-588757,PCBA-588756,PCBA-588751,PCBA-588743,PCBA-588741,PCBA-588715,PCBA-588712,PCBA-588711,PCBA-651717,PCBA-651709,PCBA-651705,PCBA-651697,PCBA-588724,PCBA-651693,PCBA-651692,PCBA-651684,PCBA-588673,PCBA-651683,PCBA-651680,PCBA-651673,PCBA-651672,PCBA-588634,PCBA-588632,PCBA-588629,PCBA-651657,PCBA-651635,PCBA-588631,PCBA-588630,PCBA-588628,PCBA-588626,PCBA-588624,PCBA-588553,PCBA-588548,PCBA-651644,PCBA-602404,PCBA-602400,PCBA-588530,PCBA-588529,PCBA-651630,PCBA-602427,PCBA-602356,PCBA-602334,PCBA-588503,PCBA-588495,PCBA-588480,PCBA-602434,PCBA-588717,PCBA-588714,PCBA-588707,PCBA-588696,PCBA-588688,PCBA-588680,PCBA-588679,PCBA-588678,PCBA-588594,PCBA-588570,PCBA-588558,PCBA-588557,PCBA-588556,PCBA-602425,PCBA-602133,PCBA-602131,PCBA-588671,PCBA-588593,PCBA-588588,PCBA-588415,PCBA-651600,PCBA-651599,PCBA-588426,PCBA-588425,PCBA-651597,PCBA-588392,PCBA-588390,PCBA-588404,PCBA-588396,PCBA-588394,PCBA-588388,PCBA-588387,PCBA-588385,PCBA-588384,PCBA-588365,PCBA-588363,PCBA-651570,PCBA-651569,PCBA-651568,PCBA-651567,PCBA-651565,PCBA-651564,PCBA-651561,PCBA-624394,PCBA-602464,PCBA-651559,PCBA-651558,PCBA-588399,PCBA-588374,PCBA-588372,PCBA-588371,PCBA-588331,PCBA-588330,PCBA-588329,PCBA-588324,PCBA-624503,PCBA-624501,PCBA-624493,PCBA-624491,PCBA-540363,PCBA-624487,PCBA-540353,PCBA-540352,PCBA-540350,PCBA-540348,PCBA-540347,PCBA-540339,PCBA-540360,PCBA-540354,PCBA-540338,PCBA-624455,PCBA-588846,PCBA-588845,PCBA-588844,PCBA-588840,PCBA-588321,PCBA-624418,PCBA-624417,PCBA-540318,PCBA-540316,PCBA-540315,PCBA-540314,PCBA-540312,PCBA-624405,PCBA-624404,PCBA-624403,PCBA-624395,PCBA-624385,PCBA-624384,PCBA-624383,PCBA-624382,PCBA-588449,PCBA-540266,PCBA-540264,PCBA-504943,PCBA-504939,PCBA-540323,PCBA-624351,PCBA-624330,PCBA-624343,PCBA-624347,PCBA-624344,PCBA-624337,PCBA-624336,PCBA-624335,PCBA-624322,PCBA-624317,PCBA-624332,PCBA-624331,PCBA-624329,PCBA-624328,PCBA-624327,PCBA-624326,PCBA-540322,PCBA-624312,PCBA-624308,PCBA-602251,PCBA-504837,PCBA-624305,PCBA-588435,PCBA-504831,PCBA-504828,PCBA-504820,PCBA-504818,PCBA-624300,PCBA-624298,PCBA-624297,PCBA-624296,PCBA-624291,PCBA-624287,PCBA-624285,PCBA-624274,PCBA-624273,PCBA-624265,PCBA-624261,PCBA-624258,PCBA-624254,PCBA-624253,PCBA-624252,PCBA-624251,PCBA-624250,PCBA-624249,PCBA-624248,PCBA-624247,PCBA-624246,PCBA-504826,PCBA-504823,PCBA-624245,PCBA-624244,PCBA-624243,PCBA-602338,PCBA-588802,PCBA-588770,PCBA-504569,PCBA-504566,PCBA-1690,PCBA-1689,PCBA-624241,PCBA-624173,PCBA-504937,PCBA-624207,PCBA-504789,PCBA-504788,PCBA-624202,PCBA-624172,PCBA-624171,PCBA-624170,PCBA-624166,PCBA-624161,PCBA-624160,PCBA-504891,PCBA-504769,PCBA-624147,PCBA-624146,PCBA-624145,PCBA-588377,PCBA-588373,PCBA-624134,PCBA-624133,PCBA-624132,PCBA-504755,PCBA-624116,PCBA-624044,PCBA-624032,PCBA-624031,PCBA-624030,PCBA-588647,PCBA-588639,PCBA-588611,PCBA-588609,PCBA-588607,PCBA-588605,PCBA-588575,PCBA-504703,PCBA-504702,PCBA-504687,PCBA-504685,PCBA-2566,PCBA-504674,PCBA-504655,PCBA-624089,PCBA-624087,PCBA-602437,PCBA-602435,PCBA-602433,PCBA-602431,PCBA-504911,PCBA-504910,PCBA-504909,PCBA-504903,PCBA-504901,PCBA-504898,PCBA-504897,PCBA-504667,PCBA-504666,PCBA-602136,PCBA-588857,PCBA-588447,PCBA-588443,PCBA-588437,PCBA-504860,PCBA-504857,PCBA-504854,PCBA-504853,PCBA-504852,PCBA-504654,PCBA-504650,PCBA-504649,PCBA-624002,PCBA-602179,PCBA-504713,PCBA-623996,PCBA-623994,PCBA-623992,PCBA-623989,PCBA-623978,PCBA-623955,PCBA-588572,PCBA-588555,PCBA-623861,PCBA-602469,PCBA-504684,PCBA-504683,PCBA-504682,PCBA-504646,PCBA-504645,PCBA-504597,PCBA-504588,PCBA-602374,PCBA-602372,PCBA-602367,PCBA-504572,PCBA-602478,PCBA-602477,PCBA-602476,PCBA-602475,PCBA-602474,PCBA-504642,PCBA-504640,PCBA-504576,PCBA-504575,PCBA-504574,PCBA-504573,PCBA-504571,PCBA-504570,PCBA-504564,PCBA-504562,PCBA-504561,PCBA-504556,PCBA-504551,PCBA-504535,PCBA-504533,PCBA-504695,PCBA-504694,PCBA-504693,PCBA-504563,PCBA-504560,PCBA-504559,PCBA-504557,PCBA-504555,PCBA-504553,PCBA-504524,PCBA-504504,PCBA-504502,PCBA-504526,PCBA-504518,PCBA-504516,PCBA-504509,PCBA-504508,PCBA-504485,PCBA-602376,PCBA-602304,PCBA-602257,PCBA-602389,PCBA-602388,PCBA-602386,PCBA-602384,PCBA-602382,PCBA-602380,PCBA-602378,PCBA-602377,PCBA-602375,PCBA-602332,PCBA-602369,PCBA-602368,PCBA-602365,PCBA-602364,PCBA-602361,PCBA-504450,PCBA-504449,PCBA-602358,PCBA-602357,PCBA-602350,PCBA-602296,PCBA-588620,PCBA-588608,PCBA-588606,PCBA-588604,PCBA-588563,PCBA-504440,PCBA-602328,PCBA-602326,PCBA-602313,PCBA-602298,PCBA-588401,PCBA-492949,PCBA-602293,PCBA-602292,PCBA-588583,PCBA-588581,PCBA-588568,PCBA-588566,PCBA-588564,PCBA-540371,PCBA-540368,PCBA-540365,PCBA-540349,PCBA-504889,PCBA-504870,PCBA-504868,PCBA-504867,PCBA-504433,PCBA-504432,PCBA-504530,PCBA-504395,PCBA-504394,PCBA-504393,PCBA-504388,PCBA-504409,PCBA-504360,PCBA-504353,PCBA-504347,PCBA-504367,PCBA-504363,PCBA-504358,PCBA-504349,PCBA-504341,PCBA-602208,PCBA-588637,PCBA-504503,PCBA-504484,PCBA-504352,PCBA-504335,PCBA-504633,PCBA-504631,PCBA-504413,PCBA-504331,PCBA-504325,PCBA-504323,PCBA-493250,PCBA-493249,PCBA-602263,PCBA-493239,PCBA-493238,PCBA-493237,PCBA-493235,PCBA-493234,PCBA-493230,PCBA-493228,PCBA-493227,PCBA-493226,PCBA-493225,PCBA-493213,PCBA-602259,PCBA-504608,PCBA-504604,PCBA-504599,PCBA-504931,PCBA-493198,PCBA-493196,PCBA-493195,PCBA-493193,PCBA-493181,PCBA-493180,PCBA-493176,PCBA-588412,PCBA-2576,PCBA-2533,PCBA-493167,PCBA-504390,PCBA-493215,PCBA-493150,PCBA-493149,PCBA-493147,PCBA-493145,PCBA-493142,PCBA-493141,PCBA-493139,PCBA-493137,PCBA-493135,PCBA-493134,PCBA-493133,PCBA-493132,PCBA-493126,PCBA-602236,PCBA-602235,PCBA-602234,PCBA-493130,PCBA-493112,PCBA-602233,PCBA-493095,PCBA-493092,PCBA-602217,PCBA-602215,PCBA-493099,PCBA-493082,PCBA-493081,PCBA-602211,PCBA-602210,PCBA-588780,PCBA-588779,PCBA-602198,PCBA-602188,PCBA-493089,PCBA-493080,PCBA-493069,PCBA-493064,PCBA-493060,PCBA-602204,PCBA-602202,PCBA-602201,PCBA-602200,PCBA-602199,PCBA-493093,PCBA-493053,PCBA-493051,PCBA-493050,PCBA-493037,PCBA-602191,PCBA-602176,PCBA-493015,PCBA-493013,PCBA-602168,PCBA-602167,PCBA-602166,PCBA-449756,PCBA-449750,PCBA-449749,PCBA-434945,PCBA-2631,PCBA-2630,PCBA-2519,PCBA-2398,PCBA-588355,PCBA-540304,PCBA-602127,PCBA-588856,PCBA-493038,PCBA-588855,PCBA-493113,PCBA-588851,PCBA-588849,PCBA-588848,PCBA-588847,PCBA-492954,PCBA-588827,PCBA-588811,PCBA-588505,PCBA-588504,PCBA-540276,PCBA-588809,PCBA-588799,PCBA-588795,PCBA-489039,PCBA-489038,PCBA-489037,PCBA-489036,PCBA-489011,PCBA-588790,PCBA-588783,PCBA-504792,PCBA-588727,PCBA-488985,PCBA-588763,PCBA-504415,PCBA-504359,PCBA-588742,PCBA-588719,PCBA-488976,PCBA-588720,PCBA-488958,PCBA-588689,PCBA-588681,PCBA-588524,PCBA-588359,PCBA-540334,PCBA-492960,PCBA-488913,PCBA-488908,PCBA-488948,PCBA-488934,PCBA-488914,PCBA-488897,PCBA-488891,PCBA-588603,PCBA-588601,PCBA-588600,PCBA-588599,PCBA-588598,PCBA-588591,PCBA-588590,PCBA-588586,PCBA-588579,PCBA-488830,PCBA-488828,PCBA-588554,PCBA-588525,PCBA-588498,PCBA-488858,PCBA-488843,PCBA-488820,PCBA-488803,PCBA-463199,PCBA-435010,PCBA-588547,PCBA-588546,PCBA-588545,PCBA-588544,PCBA-588541,PCBA-588538,PCBA-588537,PCBA-588535,PCBA-588533,PCBA-588532,PCBA-588526,PCBA-488811,PCBA-488810,PCBA-488805,PCBA-488804,PCBA-588516,PCBA-588515,PCBA-588514,PCBA-588513,PCBA-588502,PCBA-588481,PCBA-2423,PCBA-2400,PCBA-2388,PCBA-2387,PCBA-2327,PCBA-504501,PCBA-504497,PCBA-504492,PCBA-504488,PCBA-588463,PCBA-588456,PCBA-540257,PCBA-540254,PCBA-488797,PCBA-488770,PCBA-588453,PCBA-588451,PCBA-588442,PCBA-588440,PCBA-588439,PCBA-588382,PCBA-588379,PCBA-588434,PCBA-588429,PCBA-504673,PCBA-504671,PCBA-504670,PCBA-504665,PCBA-504664,PCBA-504641,PCBA-504517,PCBA-504514,PCBA-504512,PCBA-504489,PCBA-493251,PCBA-488782,PCBA-588411,PCBA-588406,PCBA-588400,PCBA-588398,PCBA-588397,PCBA-588378,PCBA-504927,PCBA-504500,PCBA-588361,PCBA-588349,PCBA-588348,PCBA-588347,PCBA-588345,PCBA-588344,PCBA-588343,PCBA-588342,PCBA-488827,PCBA-488808,PCBA-488795,PCBA-488792,PCBA-588341,PCBA-588340,PCBA-588339,PCBA-504539,PCBA-463185,PCBA-463184,PCBA-504362,PCBA-540327,PCBA-540362,PCBA-463109,PCBA-540359,PCBA-540356,PCBA-540346,PCBA-540343,PCBA-504840,PCBA-540335,PCBA-540326,PCBA-540288,PCBA-540317,PCBA-463080,PCBA-463077,PCBA-463076,PCBA-489004,PCBA-488901,PCBA-504834,PCBA-485352,PCBA-504832,PCBA-540298,PCBA-540297,PCBA-540296,PCBA-540256,PCBA-540280,PCBA-540279,PCBA-540271,PCBA-540270,PCBA-540269,PCBA-540268,PCBA-540259,PCBA-540258,PCBA-540255,PCBA-504659,PCBA-504658,PCBA-540252,PCBA-540246,PCBA-504944,PCBA-504942,PCBA-504941,PCBA-504932,PCBA-449733,PCBA-504895,PCBA-504882,PCBA-435031,PCBA-435029,PCBA-504865,PCBA-504861,PCBA-504850,PCBA-504848,PCBA-504847,PCBA-504845,PCBA-504843,PCBA-504842,PCBA-504841,PCBA-492994,PCBA-492987,PCBA-492996,PCBA-488950,PCBA-488943,PCBA-488932,PCBA-488931,PCBA-488930,PCBA-488909,PCBA-488907,PCBA-488905,PCBA-488870,PCBA-488868,PCBA-488867,PCBA-488866,PCBA-488848,PCBA-488844,PCBA-488836,PCBA-488809,PCBA-488807,PCBA-488802,PCBA-463074,PCBA-504806,PCBA-504724,PCBA-434967,PCBA-434957,PCBA-434935,PCBA-434930,PCBA-434923,PCBA-504765,PCBA-434946,PCBA-504763,PCBA-504762,PCBA-504756,PCBA-463142,PCBA-463081,PCBA-2838,PCBA-2802,PCBA-504730,PCBA-504729,PCBA-504728,PCBA-504727,PCBA-504726,PCBA-504725,PCBA-504723,PCBA-504722,PCBA-504719,PCBA-488935,PCBA-488925,PCBA-488842,PCBA-488826,PCBA-488819,PCBA-463227,PCBA-463105,PCBA-434981,PCBA-485287,PCBA-485285,PCBA-485278,PCBA-485277,PCBA-2822,PCBA-2820,PCBA-504706,PCBA-2812,PCBA-2788,PCBA-2791,PCBA-504701,PCBA-504699,PCBA-504697,PCBA-504689,PCBA-504672,PCBA-504544,PCBA-485295,PCBA-463251,PCBA-463250,PCBA-463107,PCBA-504648,PCBA-488854,PCBA-488851,PCBA-488850,PCBA-488849,PCBA-488838,PCBA-488832,PCBA-488821,PCBA-504549,PCBA-504542,PCBA-493003,PCBA-434951,PCBA-434938,PCBA-2744,PCBA-2742,PCBA-2740,PCBA-504637,PCBA-504636,PCBA-504548,PCBA-504453,PCBA-504447,PCBA-504446,PCBA-2748,PCBA-493002,PCBA-2843,PCBA-2750,PCBA-2739,PCBA-2738,PCBA-504609,PCBA-504565,PCBA-2684,PCBA-2678,PCBA-2649,PCBA-2644,PCBA-504547,PCBA-504546,PCBA-504536,PCBA-493094,PCBA-504467,PCBA-504466,PCBA-504465,PCBA-504444,PCBA-504320,PCBA-504318,PCBA-504316,PCBA-504315,PCBA-504314,PCBA-493247,PCBA-493243,PCBA-493242,PCBA-493233,PCBA-493229,PCBA-489005,PCBA-485288,PCBA-2537,PCBA-2102,PCBA-1903,PCBA-881,PCBA-852,PCBA-728,PCBA-716,PCBA-493197,PCBA-2474,PCBA-504397,PCBA-449748,PCBA-2573,PCBA-2565,PCBA-2564,PCBA-504364,PCBA-504339,PCBA-504333,PCBA-504332,PCBA-504329,PCBA-504327,PCBA-493194,PCBA-504322,PCBA-504313,PCBA-493248,PCBA-493177,PCBA-493240,PCBA-493231,PCBA-493218,PCBA-434941,PCBA-434937,PCBA-493214,PCBA-493212,PCBA-493210,PCBA-493208,PCBA-493206,PCBA-493205,PCBA-493204,PCBA-493203,PCBA-493201,PCBA-493200,PCBA-493199,PCBA-493192,PCBA-493191,PCBA-493188,PCBA-493185,PCBA-493182,PCBA-493179,PCBA-2347,PCBA-493174,PCBA-493170,PCBA-493169,PCBA-493168,PCBA-493166,PCBA-493165,PCBA-493054,PCBA-493052,PCBA-493049,PCBA-493045,PCBA-493100,PCBA-493155,PCBA-493153,PCBA-488837,PCBA-493107,PCBA-493106,PCBA-493102,PCBA-435004,PCBA-493085,PCBA-493083,PCBA-493078,PCBA-493074,PCBA-493073,PCBA-493071,PCBA-493068,PCBA-493067,PCBA-493066,PCBA-493065,PCBA-1666,PCBA-1655,PCBA-1450,PCBA-449726,PCBA-435027,PCBA-488923,PCBA-488921,PCBA-488892,PCBA-488884,PCBA-488882,PCBA-488876,PCBA-488799,PCBA-488793,PCBA-449737,PCBA-449736,PCBA-449727,PCBA-435032,PCBA-435024,PCBA-435018,PCBA-435011,PCBA-2335,PCBA-2500,PCBA-2497,PCBA-2496,PCBA-2483,PCBA-2475,PCBA-2466,PCBA-2397,PCBA-2359,PCBA-2348,PCBA-2337,PCBA-2334,PCBA-2285,PCBA-2284,PCBA-2801,PCBA-2686,PCBA-2682,PCBA-2654,PCBA-2468,PCBA-2442,PCBA-493020,PCBA-493014,PCBA-2799,PCBA-2798,PCBA-1941,PCBA-1535,PCBA-1958,PCBA-1957,PCBA-1750,PCBA-1749,PCBA-1659,PCBA-1618,PCBA-1512,PCBA-485345,PCBA-492998,PCBA-489010,PCBA-434942,PCBA-492961,PCBA-1569,PCBA-489041,PCBA-489026,PCBA-489022,PCBA-492959,PCBA-492952,PCBA-492950,PCBA-489034,PCBA-489020,PCBA-488890,PCBA-492948,PCBA-489033,PCBA-489006,PCBA-488833,PCBA-489040,PCBA-489025,PCBA-489018,PCBA-492947,PCBA-488791,PCBA-489043,PCBA-489014,PCBA-488773,PCBA-489035,PCBA-489032,PCBA-489027,PCBA-2840,PCBA-2839,PCBA-2834,PCBA-2831,PCBA-2640,PCBA-489024,PCBA-489023,PCBA-488920,PCBA-489012,PCBA-488903,PCBA-2238,PCBA-489008,PCBA-489007,PCBA-485353,PCBA-485284,PCBA-1056,PCBA-1701,PCBA-1538,PCBA-2354,PCBA-485367,PCBA-488983,PCBA-488982,PCBA-488981,PCBA-2101,PCBA-488966,PCBA-2784,PCBA-1017,PCBA-488953,PCBA-2197,PCBA-2185,PCBA-488906,PCBA-488904,PCBA-488888,PCBA-488886,PCBA-488880,PCBA-488879,PCBA-488878,PCBA-488875,PCBA-488874,PCBA-488873,PCBA-485368,PCBA-488863,PCBA-488861,PCBA-488860,PCBA-2705,PCBA-1970,PCBA-488840,PCBA-488835,PCBA-463135,PCBA-2561,PCBA-2113,PCBA-488817,PCBA-488816,PCBA-488815,PCBA-488800,PCBA-488783,PCBA-463211,PCBA-434936,PCBA-434931,PCBA-488789,PCBA-488788,PCBA-488785,PCBA-488752,PCBA-488745,PCBA-463120,PCBA-2743,PCBA-2530,PCBA-485364,PCBA-485360,PCBA-485349,PCBA-485341,PCBA-485313,PCBA-463256,PCBA-2597,PCBA-2596,PCBA-2595,PCBA-2592,PCBA-2590,PCBA-2588,PCBA-2401,PCBA-2704,PCBA-2693,PCBA-2683,PCBA-2635,PCBA-2633,PCBA-2610,PCBA-2525,PCBA-2518,PCBA-2511,PCBA-2396,PCBA-485314,PCBA-485298,PCBA-485297,PCBA-485294,PCBA-485290,PCBA-2662,PCBA-2480,PCBA-2453,PCBA-2446,PCBA-485281,PCBA-463217,PCBA-2568,PCBA-2567,PCBA-2515,PCBA-2514,PCBA-463254,PCBA-2634,PCBA-2547,PCBA-2499,PCBA-2581,PCBA-463229,PCBA-463220,PCBA-463214,PCBA-463206,PCBA-463205,PCBA-463204,PCBA-463203,PCBA-463191,PCBA-2346,PCBA-2332,PCBA-2463,PCBA-2460,PCBA-463127,PCBA-449761,PCBA-449755,PCBA-463106,PCBA-435009,PCBA-435002,PCBA-2819,PCBA-2808,PCBA-2752,PCBA-2664,PCBA-2532,PCBA-463097,PCBA-463096,PCBA-2753,PCBA-463088,PCBA-449766,PCBA-434955,PCBA-435026,PCBA-434968,PCBA-1335,PCBA-449762,PCBA-1769,PCBA-1341,PCBA-1340,PCBA-1339,PCBA-1337,PCBA-1336,PCBA-1334,PCBA-449764,PCBA-449745,PCBA-1333,PCBA-435023,PCBA-2823,PCBA-449754,PCBA-449753,PCBA-1405,PCBA-959,PCBA-958,PCBA-945,PCBA-944,PCBA-942,PCBA-923,PCBA-912,PCBA-907,PCBA-900,PCBA-897,PCBA-896,PCBA-892,PCBA-890,PCBA-889,PCBA-875,PCBA-1519,PCBA-1379,PCBA-995,PCBA-994,PCBA-993,PCBA-989,PCBA-988,PCBA-987,PCBA-986,PCBA-985,PCBA-984,PCBA-983,PCBA-982,PCBA-981,PCBA-980,PCBA-979,PCBA-978,PCBA-977,PCBA-976,PCBA-975,PCBA-974,PCBA-973,PCBA-972,PCBA-971,PCBA-970,PCBA-969,PCBA-968,PCBA-967,PCBA-966,PCBA-965,PCBA-964,PCBA-963,PCBA-962,PCBA-961,PCBA-960,PCBA-955,PCBA-948,PCBA-947,PCBA-946,PCBA-943,PCBA-939,PCBA-938,PCBA-934,PCBA-933,PCBA-931,PCBA-930,PCBA-926,PCBA-925,PCBA-924,PCBA-922,PCBA-921,PCBA-918,PCBA-917,PCBA-916,PCBA-915,PCBA-914,PCBA-910,PCBA-904,PCBA-903,PCBA-902,PCBA-899,PCBA-895,PCBA-891,PCBA-887,PCBA-885,PCBA-884,PCBA-883,PCBA-1026,PCBA-1023,PCBA-434932,PCBA-1376,PCBA-1047,PCBA-1045,PCBA-1028,PCBA-1015,PCBA-856,PCBA-854,PCBA-851,PCBA-435019,PCBA-434958,PCBA-1744,PCBA-435014,PCBA-2326,PCBA-434997,PCBA-434987,PCBA-2311,PCBA-2307,PCBA-2298,PCBA-2296,PCBA-2295,PCBA-2217,PCBA-434976,PCBA-434954,PCBA-434947,PCBA-2603,PCBA-2758,PCBA-2821,PCBA-2538,PCBA-2795,PCBA-2794,PCBA-2787,PCBA-2786,PCBA-2785,PCBA-2451,PCBA-2167,PCBA-2763,PCBA-2762,PCBA-2745,PCBA-2741,PCBA-2734,PCBA-2733,PCBA-2730,PCBA-2729,PCBA-2695,PCBA-2115,PCBA-2111,PCBA-2110,PCBA-2100,PCBA-2712,PCBA-2711,PCBA-2708,PCBA-2701,PCBA-2696,PCBA-2685,PCBA-2680,PCBA-2677,PCBA-2676,PCBA-2486,PCBA-2673,PCBA-2671,PCBA-2669,PCBA-2668,PCBA-2667,PCBA-2666,PCBA-2660,PCBA-2425,PCBA-2381,PCBA-1491,PCBA-1489,PCBA-2613,PCBA-2458,PCBA-2457,PCBA-2456,PCBA-2452,PCBA-2510,PCBA-2594,PCBA-2591,PCBA-2585,PCBA-2572,PCBA-1721,PCBA-2559,PCBA-2551,PCBA-2549,PCBA-2528,PCBA-1030,PCBA-2546,PCBA-2508,PCBA-2507,PCBA-2364,PCBA-2353,PCBA-2173,PCBA-1708,PCBA-1707,PCBA-2501,PCBA-2035,PCBA-2015,PCBA-2454,PCBA-2450,PCBA-2467,PCBA-411,PCBA-2441,PCBA-2422,PCBA-2403,PCBA-2395,PCBA-2195,PCBA-1540,PCBA-2419,PCBA-2414,PCBA-2409,PCBA-2402,PCBA-2244,PCBA-1650,PCBA-1621,PCBA-2429,PCBA-2410,PCBA-1916,PCBA-2391,PCBA-2390,PCBA-1981,PCBA-1863,PCBA-2384,PCBA-2382,PCBA-1985,PCBA-1850,PCBA-2294,PCBA-2323,PCBA-2289,PCBA-1751,PCBA-2286,PCBA-2279,PCBA-1543,PCBA-1541,PCBA-2267,PCBA-2265,PCBA-2263,PCBA-2257,PCBA-1455,PCBA-2253,PCBA-2252,PCBA-2251,PCBA-2242,PCBA-1466,PCBA-2224,PCBA-2213,PCBA-2212,PCBA-2210,PCBA-2208,PCBA-2003,PCBA-2002,PCBA-1999,PCBA-1994,PCBA-1990,PCBA-1988,PCBA-2180,PCBA-2179,PCBA-2160,PCBA-2147,PCBA-2120,PCBA-2112,PCBA-2107,PCBA-2096,PCBA-2010,PCBA-2089,PCBA-2081,PCBA-2080,PCBA-2077,PCBA-2075,PCBA-2051,PCBA-2044,PCBA-2037,PCBA-2027,PCBA-2020,PCBA-2019,PCBA-1868,PCBA-2009,PCBA-1983,PCBA-1975,PCBA-1973,PCBA-1972,PCBA-1969,PCBA-1626,PCBA-1964,PCBA-1960,PCBA-1959,PCBA-1956,PCBA-1872,PCBA-1948,PCBA-1891,PCBA-1944,PCBA-1936,PCBA-1935,PCBA-1934,PCBA-1933,PCBA-1915,PCBA-1914,PCBA-1913,PCBA-1902,PCBA-1900,PCBA-1897,PCBA-1896,PCBA-1895,PCBA-1890,PCBA-1889,PCBA-1888,PCBA-1886,PCBA-1884,PCBA-1883,PCBA-1882,PCBA-1877,PCBA-1876,PCBA-1871,PCBA-1869,PCBA-1865,PCBA-1733,PCBA-1634,PCBA-1631,PCBA-1821,PCBA-1816,PCBA-1815,PCBA-1493,PCBA-1492,PCBA-1461,PCBA-1795,PCBA-1771,PCBA-1770,PCBA-1753,PCBA-1740,PCBA-1739,PCBA-1736,PCBA-1735,PCBA-1731,PCBA-1730,PCBA-1727,PCBA-1725,PCBA-1724,PCBA-1723,PCBA-1705,PCBA-1699,PCBA-1692,PCBA-1691,PCBA-1688,PCBA-1687,PCBA-1686,PCBA-1682,PCBA-1660,PCBA-1641,PCBA-1619,PCBA-1627,PCBA-1253,PCBA-1573,PCBA-1572,PCBA-1571,PCBA-1570,PCBA-1568,PCBA-1567,PCBA-1471,PCBA-1562,PCBA-1559,PCBA-1558,PCBA-1534,PCBA-1518,PCBA-1516,PCBA-1487,PCBA-1479,PCBA-1469,PCBA-1468,PCBA-1465,PCBA-1460,PCBA-1463,PCBA-1458,PCBA-1457,PCBA-1394,PCBA-1454,PCBA-1452,PCBA-1445,PCBA-1444,PCBA-1431,PCBA-1437,PCBA-1435,PCBA-1442,PCBA-1259,PCBA-846,PCBA-1215,PCBA-1421,PCBA-1420,PCBA-1419,PCBA-1418,PCBA-1417,PCBA-1414,PCBA-1412,PCBA-787,PCBA-721,PCBA-691,PCBA-679,PCBA-711,PCBA-1324,PCBA-1399,PCBA-1398,PCBA-1397,PCBA-1396,PCBA-1392,PCBA-1272,PCBA-1252,PCBA-1361,PCBA-1330,PCBA-1328,PCBA-1327,PCBA-1322,PCBA-1320,PCBA-1275,PCBA-927,PCBA-1288,PCBA-1284,PCBA-1279,PCBA-1278,PCBA-1277,PCBA-1250,PCBA-1249,PCBA-1225,PCBA-1223,PCBA-1221,PCBA-1200,PCBA-1198,PCBA-1197,PCBA-1196,PCBA-1000,PCBA-1134,PCBA-1068,PCBA-832,PCBA-820,PCBA-825,PCBA-724,PCBA-935,PCBA-830,PCBA-949,PCBA-826,PCBA-801,PCBA-737,PCBA-733,PCBA-715,PCBA-714,PCBA-713,PCBA-831,PCBA-523,PCBA-790,PCBA-1013,PCBA-718".split(
        ",")

  def create_cid_list(self, assays_to_parse):
    """Find the union of all compounds tested across one or more assays
    """

    assay_paths = []
    cid_list = np.array([], dtype=np.int64)
    assay_no = 0
    for path, dirs, filenames in os.walk(sdf_dir):
      for dir in dirs:
        # Each directory holds a range of assay results
        joined_path = os.path.join(sdf_dir, dir)
        for path, dirs, filenames in os.walk(joined_path):
          for filename in filenames:
            assay_name = "PCBA-" + filename.replace(".csv", "")
            if assay_name not in assays_to_parse:
              continue
            file_path = os.path.join(joined_path, filename)
            df = pd.read_csv(
                file_path, usecols=["PUBCHEM_CID", "PUBCHEM_ACTIVITY_OUTCOME"])
            df = df.dropna()
            df["PUBCHEM_CID"] = df["PUBCHEM_CID"].astype(np.int64)
            assay_paths.append(file_path)
            cid_list = np.append(cid_list, df["PUBCHEM_CID"].as_matrix())
            assay_no = assay_no + 1
            if assay_no % 100 == 0:
              print(
                  "Parsed: {0} of: {1}".format(assay_no, len(assays_to_parse)))

    print("Convert to CID set")
    cid_set = np.unique(cid_list)
    return assay_paths, cid_set

  def create_overview_146(self):
    assay_list = self.pcba_146_assay_list
    self.create_assay_file(assays_to_parse=assay_list, file_name="pcba_146.csv")

  def create_overview_128(self):
    assay_list = self.pcba_128_assay_list
    self.create_assay_file(assays_to_parse=assay_list, file_name="pcba_128.csv")

  def create_overview_for_gene(self, gene_symbol):
    assays_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/genesymbol/{0}/aids/TXT".format(
        gene_symbol)
    r = requests.get(assays_url)
    assays_to_parse = [f"PCBA-{str(x)}" for x in r.text.split('\n') if len(x) > 0]
    file_name = "pcba_{0}.csv".format(gene_symbol)
    self.create_assay_file(assays_to_parse=assays_to_parse, file_name=file_name)

  def create_overview_2475(self):
    '''
    Reflects the results of query (1[TotalSidCount] : 1000000000[TotalSidCount] AND 5[ActiveSidCount] : 10000000000[ActiveSidCount] AND 0[TargetCount] : 1[TargetCount] AND "small molecule"[filt] AND "doseresponse"[filt] )
    :return:
    '''
    assays_to_parse = self.pcba_2475_assay_list
    self.create_assay_file(
        assays_to_parse=assays_to_parse, file_name="pcba_2475.csv")

  def create_assay_file(self, assays_to_parse, file_name):

    cid_start = time.time()
    assay_paths, cid_ref_list = self.create_cid_list(assays_to_parse)
    cid_end = time.time()

    print("CID length is: {0}, created in: {1} hours".format(
        cid_ref_list.size, (cid_end - cid_start) / 3600))
    print("Creating overview of {0} assays".format(len(assay_paths)))

    path_final = os.path.join(data_dir, file_name)
    assay_names = []
    cid_len = cid_ref_list.size

    all_assay_start = time.time()

    assay_results = []
    for assay_path in assay_paths:

      assay_start = time.time()

      filename = os.path.basename(assay_path)
      assay_name = "PCBA-" + filename.replace(".csv", "")
      print("Looking at: {0}".format(assay_name))

      df = pd.read_csv(
          assay_path, usecols=["PUBCHEM_CID", "PUBCHEM_ACTIVITY_OUTCOME"])
      df = df.dropna(subset=["PUBCHEM_CID", "PUBCHEM_ACTIVITY_OUTCOME"])
      if len(df.index) == 0:
        continue
      df["IS_ACTIVE"] = df["PUBCHEM_ACTIVITY_OUTCOME"] == "Active"
      df = df.rename(columns={'IS_ACTIVE': assay_name})
      df["PUBCHEM_CID"] = df["PUBCHEM_CID"].astype(int)
      df[assay_name] = df[assay_name].astype(int)
      df = df.set_index("PUBCHEM_CID")
      df = df[~df.index.duplicated(keep='last')]

      assay_results_array = array.array('i', (-1 for _ in range(0, cid_len)))
      print(assay_path)
      for i in range(0, cid_len):
        cid = cid_ref_list[i]
        val = df.get_value(cid, assay_name) if cid in df.index else -1
        assay_results_array[i] = val

      assay_names.append(assay_name)
      assay_results.append(assay_results_array)
      assay_end = time.time()
      print("Parsed: {0} in {1} seconds".format(assay_name, assay_end -
                                                assay_start))

    # Now, write out the results csv, going line by line through all molecule results
    assay_results_len = len(assay_results)

    all_assay_end = time.time()

    print(
        f"Parsed all assays in: {(all_assay_end - all_assay_start) / 3600} hours"
    )

    smiles_start = time.time()

    print("Reading in smiles info")
    with open(os.path.join(data_dir, "pubchemsmiles_tuple.pickle"), "rb") as f:
      keys, values = pickle.load(f)

    header_line = ["mol_id", ",smiles"]
    for assay_name in assay_names:
      header_line.extend((",", assay_name))
    header_line_txt = "".join(header_line)

    with open(path_final, "w+") as f_final:
      f_final.write(header_line_txt + "\n")

      for i in range(0, cid_len):
        cid = cid_ref_list[i]

            # printing the mol_id
        line_for_comp = f"CID{str(cid)}"

        # printing the SMILES
        bisect_pos = bisect_left(keys, cid, 0)
        cid_pos = bisect_pos if bisect_pos != len(
            keys) and keys[bisect_pos] == cid else -1

        if cid_pos == -1:
          continue

        line_for_comp += f",{str(values[cid_pos])}"
        for j in range(0, assay_results_len):
          val = assay_results[j][i]
          line_for_comp += "," if val == -1 else f",{str(val)}"
        f_final.write(line_for_comp + "\n")

    # Now gzip it
    with open(path_final, 'rb') as f_in:
      with gzip.open(path_final + ".gz", 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    # Now remove the intermediate csv
    os.remove(path_final)
    smiles_end = time.time()

    print(f"Smiles joined and gzip in: {(smiles_end - smiles_start) / 3600} hours")

    print(
        f"Finished creating dataset: {file_name} in: {(smiles_end - all_assay_start) / 3600} hours"
    )


parser = argparse.ArgumentParser(
    description='Deepchem dataset builder for PCBA datasets')
parser.add_argument(
    '-d',
    action='store',
    dest='dataset_name',
    default="",
    help='Choice of dataset: pcba_128, pcba_146, pcba_2475')
parser.add_argument(
    '-g',
    action='store',
    dest='gene_arg',
    default=None,
    help='Name of gene to create a dataset for')

args = parser.parse_args()
pcba_builder = PCBADatsetBuilder()
if args.dataset_name == "pcba_128":
  pcba_builder.create_overview_128()
elif args.dataset_name == "pcba_146":
  pcba_builder.create_overview_146()
elif args.dataset_name == "pcba_2475":
  pcba_builder.create_overview_2475()
elif args.gene_arg is not None:
  pcba_builder.create_overview_for_gene(args.gene_arg)
else:
  parser.print_help()
