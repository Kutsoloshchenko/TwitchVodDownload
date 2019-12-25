import threading
from VideoPartFileSaver import *
import requests


class dowloadThread (threading.Thread):
    def __init__(self, startNumber, endNumber, base_link):
        threading.Thread.__init__(self)
        self.startNumber = startNumber
        self.endNumber = endNumber
        self.base_link = base_link

    def run(self):
        for i in range(self.startNumber, self.endNumber):
            video_part = requests.get(self.base_link + str(i) + ".ts")
            if video_part.status_code == 200:
                save_video_part_file(video_part.content, str(i) + ".ts")