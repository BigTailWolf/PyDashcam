#!/usr/bin/env python3

import os, subprocess
from picamera import PiCamera
from time import sleep
from datetime import datetime

MAX_VIDEO_SAVED = 360
VIDEO_PATH = '/home/pi/Videos'
H264BUFFER = 2 # Two is enough since processing one file is taking less time than recording

def processMP4(source_name, target_name):
    # Converting the H264 into MP4
    command = "MP4Box -add {0} {1}".format(source_name, target_name)
    subprocess.Popen(command, shell = True)

    # Delete in Rotation if MP4 files are over the maxmium count
    files = os.listdir(VIDEO_PATH)
    mp4files = sorted([f for f in files if f.endswith('.mp4')])
    print(mp4files)
    delete_count = len(mp4files) - MAX_VIDEO_SAVED
    if delete_count > 0:
        for v in mp4files[:delete_count]:
            os.remove('{0}/{1}'.format(VIDEO_PATH, v))


def main():
    camera = PiCamera()
    camera.resolution = (1920, 1080)
    camera.start_preview()
    index = 0

    while True:
        time_stamp   = datetime.now().isoformat().split('.')[0]
        h264filename = '{0}/capture.{1}.h264'.format(VIDEO_PATH, index)
        mp4filename  = '{0}/{1}.mp4'.format(VIDEO_PATH, time_stamp)

        camera.start_recording(h264filename)
        for i in range(30):
            ticks = datetime.now()
            camera.annotate_text = ticks.isoformat().split('.')[0]
            sleep(1)

        camera.stop_recording()
        processMP4(h264filename, mp4filename)
        index = (index + 1) % H264BUFFER

    camera.stop_preview()

# Main function starts
if __name__ == '__main__':
    main()

