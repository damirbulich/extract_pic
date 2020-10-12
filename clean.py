import argparse as arg
import glob
import os.path as path
import os

parser = arg.ArgumentParser(
    description="Delete unlabeled images"
)
parser.add_argument(
    "dir",
    metavar="Dir",
    type=str,
    help="path to directory containing images",
)
parser.add_argument(
    "--type", type=str, default="jpg", help="file type [jpg/png]"
)

args = parser.parse_args()

if path.isdir(args.dir):
    images = glob.glob("{}/*.{}".format(args.dir, args.type))
    counter = 0
    for image in images:
        if not os.path.isfile(".".join(image.split(".")[:-1]) + ".json"):
            os.remove(image)
            counter +=1
    print("Deleted {} unlabeled images!".format(counter))

else:
    print("Directory not found!")
