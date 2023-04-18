from database import get_mysql_db
import resizer
import upscaler
import argparse
import os
import glob
import cv2
import logging
import time
import shutil

INPUT_FOLDER = f"E:/new-fifty-images-resized"
DB_HOST = "dev-public-2021-11-02-cluster.cluster-collu5gxyjqo.us-east-1.rds.amazonaws.com"
# DB_HOST = "prod-from-backup-2020-10-16-cluster.cluster-collu5gxyjqo.us-east-1.rds.amazonaws.com"
DB_USER = "flower"
DB_PASS = "50-honor-fold-roister-measure"
logging.basicConfig(level='INFO', format='%(asctime)s [%(name)16s] %(levelname)-8s %(message)s')
logger = logging.getLogger("image-validator")


def main():
    db_images = get_db_images()
    count = 0

    local_images = sorted(glob.glob(os.path.join(INPUT_FOLDER, '*')))
    for img in db_images:
        localname = img.split(".")[:-1]
        localname = ".".join(localname) + ".webp"
        newbytesize = os.stat(f"{INPUT_FOLDER}/{localname}").st_size
        update_in_db(img, newbytesize)
        count += 1
        logger.info(f"Updated {img} ({count}/{len(db_images)})")

        if count % 1000 == 0:
            conn.commit()
    conn.commit()
    # local_images = [x.split("\\")[-1] for x in local_images]
    # for img in db_images:
    #     newimg = img.split(".")[:-1]
    #     newimg = ".".join(newimg) + ".webp"
    #     if newimg not in local_images:
    #         logger.warning(f"This image is not found in the folder {newimg}")
    #         count += 1
    # logger.info(f"{count} images not found in the folder")

    # db_images = [".".join(x.split(".")[:-1])+".webp" for x in db_images]
    # for img in local_images:
    #     if img not in db_images:
    #         logger.warning(f"This image is not found in the db {img}")
    #         shutil.move(f"{INPUT_FOLDER}/{img}","E:/")
    #         count += 1
    #
    # logger.info(f"{count} images not found in the db")


def update_in_db(name, size):
    sql = f"UPDATE image_optimizer_cleanup SET new_bytesize={size} WHERE image_name=%s"
    logger.info(sql, name)
    cursor.execute(sql, (name,))


def get_db_images():
    images = []
    sql = "SELECT image_name FROM image_optimizer_cleanup WHERE active=1 AND extension != 'gif' AND new_bytesize IS NULL"
    cursor.execute(sql)
    for row in cursor.fetchall():
        images.append(row[0])
    return images


if __name__ == '__main__':
    start = time.time()
    conn = get_mysql_db(host=DB_HOST, db="flowersCmsCart", user=DB_USER, pwd=DB_PASS, ssl=False)
    cursor = conn.cursor()
    main()
    if conn:
        conn.close()
    logger.info(f"Finished in {round(time.time() - start, 3)} seconds")
