from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite


def data_processing(address):
    name = address.split("/")[-1].split(".")[0]
    text_file = open("resources/results/" + name + ".txt", "w")
    with open(address) as reader:
        tle_list = reader.readlines()

    for i in range(0, len(tle_list), 4):
        line_first = tle_list[i].rstrip()
        line_second = tle_list[i + 2].rstrip()

        satellite = EarthSatellite(line_first, line_second, name, ts)
        geocentric = satellite.at(satellite.epoch)

        text_file.write(str(satellite) + "\n")
        text_file.write(str(geocentric.position.km) + "\n")
        text_file.write("in sunlight\n" if geocentric.is_sunlit(eph) else "in shadow\n")
        text_file.write("\n")


def preparatory_function(address_array):
    for address in address_array:
        data_processing(address)


ts = load.timescale()
eph = load('de421.bsp')
address_array = ["resources/202307_GRBAlpha_tle.txt", "resources/202307_Monitor-2_tle.txt",
                 "resources/202307_Monitor-3_tle.txt", "resources/202307_Monitor-4_tle.txt",
                 "resources/202307_VZLUSAT-2_tle.txt"]

preparatory_function(address_array)


