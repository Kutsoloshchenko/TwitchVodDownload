import requests
import re
from ffmpy import FFmpeg
from M3u8FileParcer import *
from VideoPartFileSaver import *
from MultiThreadSupport import *
import sys

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
CLIENT_ID_RE = r'"Client-ID":"\w+"'

TWITCH_API = "https://api.twitch.tv/api/vods/"
ACCESS_TOKEN_LINE = "/access_token?oauth_token=undefined&need_https=true&platform=web&player_type=site&player_backend=mediaplayer"

LIST_FILE_API = "https://usher.ttvnw.net/vod/"
LIST_FILE_EXTENTION = ".m3u8?"
MASTER_FILE_NAME = "index-dvr.m3u8"

def download_video(url):
    twitch_video_number = url.split("/")[-1]

    twitch_response = requests.get(url, HEADERS)

    if (twitch_response.status_code != 200):
        print("Could not get OK response from twitch")
        return

    try:
        html_string = twitch_response.content.decode()
    except:
        print("Could not decode html from Twitch, try aging mate")

    client_line = re.findall(CLIENT_ID_RE, html_string)

    if len(client_line) == 0:
        print("Could not find Client Id from Twitch. Its needed to dowload video")
        return

    client_id = client_line[0].split(":")[-1].replace('"', '')

    HEADERS['Client-ID'] = client_id
    twitch_token_response = requests.get(TWITCH_API+twitch_video_number+ACCESS_TOKEN_LINE, headers=HEADERS)

    if twitch_token_response.status_code != 200:
        "It failed mate, while was getting token"
        return
    token = twitch_token_response.json()

    media_list_request = requests.get(LIST_FILE_API + twitch_video_number + LIST_FILE_EXTENTION
                                      + "sig=" + token["sig"] + "&token=" + token["token"], headers=HEADERS)

    if media_list_request.status_code != 200:
        print("This media does not exist mate. Or i dont know, i could not download main list file")
        return

    desired_link = parce_m3u8_list_file(media_list_request.content.decode())

    if desired_link == False:
        print("Could not get link for some reason.")
        return

    master_file_request = requests.get(desired_link)

    if master_file_request.status_code != 200:
        print("Link was found but master file could not be dowloaded :(")
        return

    MASTER_FILE_NAME = desired_link.split("/")[-1]

    save_video_part_file(master_file_request.content, MASTER_FILE_NAME)

    number = parce_m3u8_master_file(master_file_request.content.decode())

    if number == 0:
        print("Could not parse number of files that required for dowloading")
        return

    link = desired_link.replace(MASTER_FILE_NAME, "")

    number_of_parts_to_save = number // 100

    thread_list = []
    starting_point = 0

    for i in range(101):

        points_to_save = i*number_of_parts_to_save

        if (points_to_save - number) > 0:
            points_to_save = number

        thread = dowloadThread(starting_point, points_to_save, link)

        thread_list.append(thread)

        starting_point = points_to_save

    for i in thread_list:
        i.start()

    for t in thread_list:
        t.join()

    try:
        ff = FFmpeg(inputs ={MASTER_FILE_NAME: None}, outputs = {twitch_video_number + '.mp4' : '-bsf:a aac_adtstoasc -c copy'})
        ff.run()
    except:
        print("Could not create the files, something went completely wrong")

    delete_file(MASTER_FILE_NAME)

    for i in range(number + 1):
       delete_file(str(i) + ".ts")
