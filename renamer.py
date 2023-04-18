import logging
import glob
import os
import shutil

INPUT_FOLDER = f"E:/new-fifty-images"
logging.basicConfig(level='INFO', format='%(asctime)s [%(name)16s] %(levelname)-8s %(message)s')
logger = logging.getLogger("image-renamer")


def main():
    images = sorted(glob.glob(os.path.join(INPUT_FOLDER, '*')))
    count = 0
    for image in images:
        fullname = image.split("\\")[-1]
        new_name = fullname
        path = f"{INPUT_FOLDER}/{fullname}"
        image_name = fullname.split(".", 1)[0]

        if fullname.endswith("_out.png"):
            new_name = fullname.replace("_out.png", ".png")
        newpath = f"{INPUT_FOLDER}/{new_name}"
        logger.info(path)
        logger.info(newpath)
        shutil.move(path, newpath)
        count += 1
        logger.info(f"Renaming {count}/{len(images)}")


main()
