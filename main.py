import resizer
import upscaler
import argparse
import os
import glob
import cv2
import logging
import time
import shutil
#
INPUT_FOLDER = "E:/input"
OUTPUT_FOLDER = "E:/output"
TEMP_FOLDER = "E:/temp"
THUMB_FOLDER = "E:/thumbnails"
DUMP_FOLDER = "E:/done"

logging.basicConfig(level='INFO', format='%(asctime)s [%(name)16s] %(levelname)-8s %(message)s')
logger = logging.getLogger("image-optimizer")

TOTAL = 16675


def main():
    images = []
    # Prepare input images from a folder
    if os.path.isfile(INPUT_FOLDER):
        paths = [INPUT_FOLDER]
    else:
        paths = sorted(glob.glob(os.path.join(INPUT_FOLDER, '*')))

    count = 0
    logger.info(f"To be processed {len(paths)}")
    for imgpath in paths:
        imgname, extension = os.path.splitext(os.path.basename(imgpath))
        fullname = f"{imgname}{extension}"
        img = cv2.imread(imgpath, cv2.IMREAD_UNCHANGED)
        if img is not None:
            width = img.shape[0]

            if width > 1024:
                shutil.copy(f"{INPUT_FOLDER}/{fullname}", f"{DUMP_FOLDER}/{fullname}")
                shutil.move(f"{INPUT_FOLDER}/{fullname}", f"{TEMP_FOLDER}/{fullname}")
            else:
                images.append((img, imgname, extension))
                count += 1
                if count % 5000 == 0:
                    break
        else:
            logger.warning(f"image {fullname} has no shape, gif?")
        # logger.info(f"{count}/{len(paths)} = {TOTAL} processed images")

    upscaler.upscale(images, INPUT_FOLDER, TEMP_FOLDER, DUMP_FOLDER, args)
    # resizer.resize(TEMP_FOLDER, OUTPUT_FOLDER, THUMB_FOLDER)


if __name__ == '__main__':
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--suffix', type=str, default='out', help='Suffix of the restored image')
    parser.add_argument('--pre_pad', type=int, default=0, help='Pre padding size at each border')
    parser.add_argument('--tile', type=int, default=0, help='Tile size, 0 for no tile during testing')
    parser.add_argument('--tile_pad', type=int, default=10, help='Tile padding')
    parser.add_argument('--ext', type=str, default='webp', help='Image extension. Options: auto | jpg | png, auto means using the same extension as inputs')
    parser.add_argument("--resize", action="store_true", help="Runs only resizing.")

    args = parser.parse_args()

    main()
    logger.info(f"Finished in {round(time.time() - start, 3)} seconds")
