import copy as cp
import numpy as np
from int_computer import IntComputer

networkpc_program = [3,62,1001,62,11,10,109,2267,105,1,0,1590,1977,876,1120,1188,2230,641,1155,1559,936,1847,2189,2117,1029,674,1917,1363,610,1695,1880,2049,1814,1493,1258,705,810,967,905,845,1662,2014,1394,1089,1631,2150,1427,1332,1524,1291,2080,1460,1730,1948,571,1221,742,1060,777,1761,998,0,0,0,0,0,0,0,0,0,0,0,0,3,64,1008,64,-1,62,1006,62,88,1006,61,170,1106,0,73,3,65,21001,64,0,1,21001,66,0,2,21101,0,105,0,1105,1,436,1201,1,-1,64,1007,64,0,62,1005,62,73,7,64,67,62,1006,62,73,1002,64,2,133,1,133,68,133,102,1,0,62,1001,133,1,140,8,0,65,63,2,63,62,62,1005,62,73,1002,64,2,161,1,161,68,161,1102,1,1,0,1001,161,1,169,102,1,65,0,1102,1,1,61,1102,1,0,63,7,63,67,62,1006,62,203,1002,63,2,194,1,68,194,194,1006,0,73,1001,63,1,63,1105,1,178,21102,1,210,0,106,0,69,2102,1,1,70,1101,0,0,63,7,63,71,62,1006,62,250,1002,63,2,234,1,72,234,234,4,0,101,1,234,240,4,0,4,70,1001,63,1,63,1105,1,218,1105,1,73,109,4,21102,0,1,-3,21102,0,1,-2,20207,-2,67,-1,1206,-1,293,1202,-2,2,283,101,1,283,283,1,68,283,283,22001,0,-3,-3,21201,-2,1,-2,1106,0,263,21202,-3,1,-3,109,-4,2105,1,0,109,4,21101,1,0,-3,21102,0,1,-2,20207,-2,67,-1,1206,-1,342,1202,-2,2,332,101,1,332,332,1,68,332,332,22002,0,-3,-3,21201,-2,1,-2,1105,1,312,21201,-3,0,-3,109,-4,2105,1,0,109,1,101,1,68,359,20102,1,0,1,101,3,68,366,21002,0,1,2,21102,1,376,0,1105,1,436,21202,1,1,0,109,-1,2106,0,0,1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304,8388608,16777216,33554432,67108864,134217728,268435456,536870912,1073741824,2147483648,4294967296,8589934592,17179869184,34359738368,68719476736,137438953472,274877906944,549755813888,1099511627776,2199023255552,4398046511104,8796093022208,17592186044416,35184372088832,70368744177664,140737488355328,281474976710656,562949953421312,1125899906842624,109,8,21202,-6,10,-5,22207,-7,-5,-5,1205,-5,521,21101,0,0,-4,21101,0,0,-3,21102,51,1,-2,21201,-2,-1,-2,1201,-2,385,470,21001,0,0,-1,21202,-3,2,-3,22207,-7,-1,-5,1205,-5,496,21201,-3,1,-3,22102,-1,-1,-5,22201,-7,-5,-7,22207,-3,-6,-5,1205,-5,515,22102,-1,-6,-5,22201,-3,-5,-3,22201,-1,-4,-4,1205,-2,461,1106,0,547,21101,-1,0,-4,21202,-6,-1,-6,21207,-7,0,-5,1205,-5,547,22201,-7,-6,-7,21201,-4,1,-4,1105,1,529,21201,-4,0,-7,109,-8,2106,0,0,109,1,101,1,68,564,20101,0,0,0,109,-1,2106,0,0,1101,0,96059,66,1102,1,5,67,1101,0,598,68,1101,0,302,69,1101,0,1,71,1101,608,0,72,1106,0,73,0,0,0,0,0,0,0,0,0,0,29,96377,1102,1,25589,66,1102,1,1,67,1101,637,0,68,1102,556,1,69,1102,1,1,71,1102,639,1,72,1105,1,73,1,-11,11,381354,1101,0,38861,66,1102,1,2,67,1102,1,668,68,1101,302,0,69,1102,1,1,71,1102,672,1,72,1105,1,73,0,0,0,0,21,40063,1102,10091,1,66,1102,1,1,67,1102,1,701,68,1101,556,0,69,1102,1,1,71,1102,703,1,72,1105,1,73,1,41,5,14897,1101,69697,0,66,1101,4,0,67,1101,732,0,68,1102,253,1,69,1101,1,0,71,1101,0,740,72,1105,1,73,0,0,0,0,0,0,0,0,7,24281,1102,1,72893,66,1101,0,1,67,1102,1,769,68,1102,556,1,69,1101,0,3,71,1101,771,0,72,1105,1,73,1,13,44,248277,11,190677,19,15556,1101,66851,0,66,1101,2,0,67,1101,804,0,68,1102,302,1,69,1101,0,1,71,1102,1,808,72,1106,0,73,0,0,0,0,34,409468,1102,46681,1,66,1101,0,1,67,1102,837,1,68,1101,0,556,69,1102,3,1,71,1102,1,839,72,1105,1,73,1,5,39,57487,39,114974,38,95138,1101,7883,0,66,1102,1,1,67,1101,872,0,68,1101,0,556,69,1102,1,1,71,1102,874,1,72,1105,1,73,1,677,43,192118,1102,1,84089,66,1101,0,1,67,1101,0,903,68,1102,1,556,69,1102,0,1,71,1102,1,905,72,1106,0,73,1,1634,1101,20297,0,66,1102,1,1,67,1101,0,932,68,1102,1,556,69,1102,1,1,71,1101,934,0,72,1106,0,73,1,967,3,23362,1102,1,95597,66,1102,1,1,67,1102,1,963,68,1102,556,1,69,1102,1,1,71,1102,1,965,72,1106,0,73,1,-231,19,11667,1101,45181,0,66,1102,1,1,67,1101,994,0,68,1102,1,556,69,1101,0,1,71,1101,996,0,72,1105,1,73,1,125,39,172461,1102,19087,1,66,1102,1,1,67,1101,0,1025,68,1102,556,1,69,1101,1,0,71,1101,1027,0,72,1106,0,73,1,51,30,103991,1102,56093,1,66,1102,1,1,67,1102,1056,1,68,1101,0,556,69,1101,1,0,71,1102,1,1058,72,1105,1,73,1,10181,12,18061,1102,69857,1,66,1102,1,1,67,1102,1,1087,68,1101,0,556,69,1101,0,0,71,1101,1089,0,72,1105,1,73,1,1387,1101,53881,0,66,1101,1,0,67,1101,1116,0,68,1102,556,1,69,1102,1,1,71,1102,1,1118,72,1106,0,73,1,37,43,288177,1102,1,11681,66,1101,3,0,67,1102,1147,1,68,1102,1,302,69,1101,0,1,71,1102,1,1153,72,1105,1,73,0,0,0,0,0,0,34,307101,1102,1,24281,66,1102,1,2,67,1102,1,1182,68,1102,351,1,69,1101,1,0,71,1101,1186,0,72,1105,1,73,0,0,0,0,255,65183,1102,1,1093,66,1101,2,0,67,1102,1,1215,68,1101,302,0,69,1102,1,1,71,1101,0,1219,72,1105,1,73,0,0,0,0,31,24671,1102,82759,1,66,1102,4,1,67,1102,1,1248,68,1101,0,302,69,1101,1,0,71,1102,1,1256,72,1106,0,73,0,0,0,0,0,0,0,0,34,204734,1101,100279,0,66,1102,1,1,67,1101,1285,0,68,1102,556,1,69,1102,2,1,71,1101,0,1287,72,1105,1,73,1,2,38,190276,38,237845,1102,1,47569,66,1101,0,6,67,1101,0,1318,68,1102,1,302,69,1102,1,1,71,1102,1330,1,72,1105,1,73,0,0,0,0,0,0,0,0,0,0,0,0,7,48562,1102,13163,1,66,1101,0,1,67,1102,1359,1,68,1101,556,0,69,1102,1,1,71,1102,1361,1,72,1106,0,73,1,293,5,44691,1102,1,101287,66,1102,1,1,67,1102,1,1390,68,1101,0,556,69,1101,0,1,71,1102,1392,1,72,1106,0,73,1,97,11,317795,1101,24671,0,66,1101,0,2,67,1102,1,1421,68,1101,0,302,69,1102,1,1,71,1102,1425,1,72,1105,1,73,0,0,0,0,47,133702,1102,77687,1,66,1101,2,0,67,1102,1,1454,68,1102,1,302,69,1102,1,1,71,1102,1,1458,72,1106,0,73,0,0,0,0,43,384236,1102,78367,1,66,1102,1,1,67,1101,1487,0,68,1101,0,556,69,1101,2,0,71,1101,0,1489,72,1106,0,73,1,10,39,229948,38,47569,1102,1,3061,66,1101,1,0,67,1101,1520,0,68,1102,556,1,69,1101,0,1,71,1101,1522,0,72,1105,1,73,1,523,30,207982,1101,33181,0,66,1102,3,1,67,1101,1551,0,68,1101,0,302,69,1101,0,1,71,1101,1557,0,72,1106,0,73,0,0,0,0,0,0,24,278788,1101,102181,0,66,1101,1,0,67,1102,1586,1,68,1101,0,556,69,1101,1,0,71,1102,1588,1,72,1106,0,73,1,378,44,165518,1101,65183,0,66,1101,0,1,67,1102,1617,1,68,1102,556,1,69,1101,0,6,71,1101,0,1619,72,1106,0,73,1,25255,29,192754,18,141326,18,211989,37,33181,37,66362,37,99543,1101,88799,0,66,1102,1,1,67,1102,1,1658,68,1101,556,0,69,1101,0,1,71,1101,1660,0,72,1106,0,73,1,160,38,285414,1102,96377,1,66,1102,1,2,67,1101,1689,0,68,1102,1,302,69,1101,0,1,71,1102,1,1693,72,1106,0,73,0,0,0,0,24,139394,1101,70663,0,66,1102,3,1,67,1101,0,1722,68,1101,0,302,69,1102,1,1,71,1102,1728,1,72,1106,0,73,0,0,0,0,0,0,24,209091,1102,104173,1,66,1101,1,0,67,1101,0,1757,68,1101,556,0,69,1102,1,1,71,1101,1759,0,72,1106,0,73,1,31,44,82759,1101,92951,0,66,1102,1,1,67,1101,0,1788,68,1101,556,0,69,1101,0,12,71,1102,1,1790,72,1106,0,73,1,1,44,331036,30,311973,4,2186,31,49342,47,66851,3,11681,12,36122,6,77722,21,80126,35,155374,43,480295,19,7778,1102,40063,1,66,1102,2,1,67,1101,0,1841,68,1101,302,0,69,1102,1,1,71,1102,1,1845,72,1106,0,73,0,0,0,0,35,77687,1102,1,74377,66,1101,1,0,67,1101,0,1874,68,1102,1,556,69,1101,2,0,71,1101,1876,0,72,1105,1,73,1,19,11,127118,19,3889,1102,3889,1,66,1102,4,1,67,1102,1,1907,68,1102,302,1,69,1102,1,1,71,1101,1915,0,72,1106,0,73,0,0,0,0,0,0,0,0,18,70663,1102,1,8353,66,1102,1,1,67,1102,1944,1,68,1101,0,556,69,1101,0,1,71,1101,0,1946,72,1106,0,73,1,-52,3,35043,1101,0,31477,66,1101,0,1,67,1102,1,1975,68,1101,0,556,69,1101,0,0,71,1102,1977,1,72,1106,0,73,1,1229,1102,32159,1,66,1102,1,1,67,1101,2004,0,68,1102,556,1,69,1101,4,0,71,1102,1,2006,72,1105,1,73,1,7,5,29794,5,59588,11,63559,43,96059,1101,0,103991,66,1102,1,3,67,1101,2041,0,68,1102,302,1,69,1101,0,1,71,1102,2047,1,72,1106,0,73,0,0,0,0,0,0,34,511835,1101,0,78157,66,1101,1,0,67,1102,2076,1,68,1102,556,1,69,1101,1,0,71,1102,2078,1,72,1106,0,73,1,-81047,4,1093,1102,57487,1,66,1101,0,4,67,1101,0,2107,68,1102,1,302,69,1101,0,1,71,1102,2115,1,72,1106,0,73,0,0,0,0,0,0,0,0,38,142707,1102,18061,1,66,1101,0,2,67,1102,2144,1,68,1102,302,1,69,1101,1,0,71,1102,1,2148,72,1105,1,73,0,0,0,0,6,38861,1102,102367,1,66,1102,5,1,67,1101,0,2177,68,1102,253,1,69,1101,1,0,71,1102,1,2187,72,1105,1,73,0,0,0,0,0,0,0,0,0,0,11,254236,1102,1,63559,66,1101,6,0,67,1102,1,2216,68,1102,1,302,69,1102,1,1,71,1102,2228,1,72,1106,0,73,0,0,0,0,0,0,0,0,0,0,0,0,24,69697,1102,14897,1,66,1101,0,4,67,1101,2257,0,68,1101,0,302,69,1101,0,1,71,1102,2265,1,72,1106,0,73,0,0,0,0,0,0,0,0,34,102367]

# initialize the network bots
my_network_bots = []
for i in range(50):
    bot = IntComputer(cp.deepcopy(networkpc_program))
    bot.extend_memory(10000)
    bot.run_cycle_network([i])
    bot.run_cycle_network([-1])
    if len(bot.get_output()) > 0:
        test = np.array(bot.get_output()).reshape(((len(bot.get_output())//3), 3))
        # print(test[0][0])
    my_network_bots.append(bot)

# prepare for repeated runnun of the network bots
package_255_received = False
nat = []
nat_ys_received = []
identical_nat_reception = False
while not identical_nat_reception:
    packages = {}
    # read outputs
    for i in range(50):
        bot = my_network_bots[i]
        output_generated = bot.get_output()
        if len(output_generated) > 0:
            bot.clear_output()
            network_packets = np.array(output_generated, dtype='int64').reshape(((len(output_generated)//3), 3))
            for packet in network_packets:
                target_address = packet[0]
                try:
                    packages[target_address] = packages[target_address] + [packet[1], packet[2]]
                except KeyError:
                    packages[target_address] = [packet[1], packet[2]]
    # for part 1: check if anything is sent to address 255: the Y value is your solution
    if 255 in packages.keys():
        nat = [packages[255][-2], packages[255][-1]]
        if not package_255_received:
            print("Solution part 1:", nat[1])
            package_255_received = True

    # for part 2: if there are no packages / outputs, send the last one received on the net to address 0
    if len(packages) == 0:
        # print("Delivering package", nat, "to address 0")
        packages[0] = nat
        if nat[1] in nat_ys_received:
            print("Solution part 2: ", nat[1])
            identical_nat_reception = True
        else:
            nat_ys_received.append(nat[1])

    for i in range(50):
        bot = my_network_bots[i]
        if i in packages.keys():
            new_input = packages[i]
        else:
            new_input = [-1]
        bot.run_cycle_network(new_input)


