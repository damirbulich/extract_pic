import cv2
import os
from math import floor
import argparse as arg
import platform


class Timestamp:
    def __init__(self, n):
        self.n = n

    def __str__(self):
        return "{:02d}-{:02d}-{:02d}".format(
            (self.n // 24) // 60, (self.n // 24) % 60, self.n % 24
        )

    def __int__(self):
        return self.n

    @staticmethod
    def fromTimestamp(timest):
        n = int(timest.split(":")[0]) * 60 * 24 + int(timest.split(":")[1]) * 24
        return Timestamp(n)


parser = arg.ArgumentParser(
    description="Extract images from video based on specified frequency."
)
parser.add_argument(
    "filename",
    metavar="File",
    type=str,
    help="path to video [video.mp4] [/path/to/video.mp4]",
)
parser.add_argument(
    "--begin", type=str, default="0:00", help="when to start extracting images [0:00]"
)
parser.add_argument(
    "--end",
    type=str,
    default="999999:00",
    help="when to stop extracting images [0:00]",
)
parser.add_argument("--fr", type=int, default=24, help="framerate of video")
parser.add_argument(
    "--freq",
    type=float,
    default=0.5,
    help="how many times a second to capture a image",
)

args = parser.parse_args()
# print(args)

filename = args.filename
if not os.path.isfile(filename):
    print("\nNo such file exists!\n")
    exit()
begin = int(Timestamp.fromTimestamp(args.begin))
# print("begin = {}".format(begin))
end = int(Timestamp.fromTimestamp(args.end))
# print("end = {}".format(end))
framerate = args.fr
freq = args.freq
timestamp = 0
cap = cv2.VideoCapture(filename)
directory = "{}".format(".".join(filename.split(".")[:-1]))
os.makedirs(directory, exist_ok=True)

while cap.isOpened():
    ret, frame = cap.read()
    if timestamp % floor(framerate / freq) == 0 and timestamp >= begin:
        name = os.path.join(
            directory, "capture_{}.jpg".format(str(Timestamp(timestamp)))
        )
        if not cv2.imwrite(name, frame):
            raise Exception("Could not write image")
    timestamp += 1
    if not ret or timestamp > end:
        break

print("\nImages saved to folder {}".format(directory))
print("That's all folks!\n")

cap.release()
