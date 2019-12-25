import re

ALL_LINKS_RE = r'https\S+'
RESOLUTION_RE = r'\d+p\d+'

def parce_m3u8_list_file(string):

    allLinks = re.findall(ALL_LINKS_RE, string)

    if len(allLinks) == 0:
        print("No links were parsed from provided info")
        return False

    desired_resolution = (360, 30)

    for i in allLinks:
        resolution = re.findall(RESOLUTION_RE, i)
        if len(resolution) == 0:
            continue

        resolution = resolution[0].split("p")

        if int(resolution[0]) > desired_resolution[0]:
            desired_resolution = (int(resolution[0]), int(resolution[1]))
        elif int(resolution[0]) == desired_resolution[0]:
            if int(resolution[1]) > desired_resolution[1]:
                desired_resolution = (int(resolution[0]), int(resolution[1]))

    for i in allLinks:
        if (i.find(str(desired_resolution[0]) + "p" + str(desired_resolution[1]))):
            return i

    return False


def parce_m3u8_master_file(string):

    lines = string.split("\n")
    lines.reverse()

    for i in lines:
        if i.find(".ts") != - 1:
            number = i.replace(".ts", "")
            try:
                return_number = int(number)
            except:
                continue

            return return_number

    return False