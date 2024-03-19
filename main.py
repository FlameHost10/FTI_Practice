from datetime import datetime

from skyfield.api import load

from functions import *

#
# def data_processing(address):
#     name = address.split("/")[-1].split(".")[0]
#     text_file = open("resources/results/" + name + ".txt", "w")
#     with open(address) as reader:
#         tle_list = reader.readlines()
#
#     for i in range(0, len(tle_list), 4):
#         line_first = tle_list[i].rstrip()
#         line_second = tle_list[i + 2].rstrip()
#
#         satellite = EarthSatellite(line_first, line_second, name, ts)
#         geocentric = satellite.at(satellite.epoch)
#
#         text_file.write(str(satellite) + "\n")
#         text_file.write(str(geocentric.position.km) + "\n")
#         text_file.write("in sunlight\n" if geocentric.is_sunlit(eph) else "in shadow\n")
#         text_file.write("\n")
#
#
# def preparatory_function(address_array):
#     if not os.path.exists("resources/results"):
#         os.mkdir("resources/results")
#     for address in address_array:
#         data_processing(address)


address_array = ["resources/202307_GRBAlpha_tle.txt", "resources/202307_Monitor-2_tle.txt",
                 "resources/202307_Monitor-3_tle.txt", "resources/202307_Monitor-4_tle.txt",
                 "resources/202307_VZLUSAT-2_tle.txt"]


ts = load.timescale()
utc_time = ts.utc(2023, 7, 20)
epoch_time = utc_time.tt

print(time_coordinates_cubesat(epoch_time, address_array[0]))



