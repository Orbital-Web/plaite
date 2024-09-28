import os
import shutil

import cv2


def convert_to_yolo_format(class_id, x1, y1, x2, y2, img_width, img_height, filename):
    center_x = (x1 + x2) / (2 * img_width)
    center_y = (y1 + y2) / (2 * img_height)
    width = (x2 - x1) / img_width
    height = (y2 - y1) / img_height
    # try:
    #     assert center_x <= 1
    #     assert center_y <= 1
    #     assert width <= 1
    #     assert height <= 1
    # except AssertionError as e:
    #     center_x = (x1 + x2) / (2 * img_width)
    #     center_y = (y1 + y2) / (2 * img_height)
    #     width = (x2 - x1) / img_width
    #     height = (y2 - y1) / img_height
    #     print(
    #         center_x,
    #         center_y,
    #         width,
    #         height,
    #         x1,
    #         x2,
    #         y1,
    #         y2,
    #         img_width,
    #         img_height,
    #         filename,
    #     )
    #     raise e
    return f"{class_id} {center_x} {center_y} {width} {height}\n"


# Set directories
data_dir = "./UECFOOD100/"
image_dir = "./yolofood/datasets/images/"
label_dir = "./yolofood/datasets/labels/"
TRAIN_RAT = 0.8
VAL_RAT = 0.1

# os.makedirs(label_dir, exist_ok=True)

for folder in os.listdir(data_dir):
    if os.path.isdir(os.path.join(data_dir, folder)):
        category = int(folder) - 1

        with open(os.path.join(data_dir, folder, "bb_info.txt")) as f:
            next(f)  # skip header
            bboxes = [[int(b) for b in bbox.split()] for bbox in f]

            train_until = int(len(bboxes) * TRAIN_RAT)
            val_until = int(len(bboxes) * (TRAIN_RAT + VAL_RAT))

            for i, bbox in enumerate(bboxes):
                fol = "train" if i < train_until else "val" if i < val_until else "test"
                fname = str(bbox[0])
                imgpath = os.path.join(data_dir, folder, fname + ".jpg")
                labelpath = os.path.join(label_dir, fol, fname + ".txt")
                img = cv2.imread(imgpath)
                label = convert_to_yolo_format(
                    category, *bbox[1:], *img.shape[:2][::-1], imgpath
                )
                shutil.copyfile(imgpath, os.path.join(image_dir, fol, fname + ".jpg"))
                with open(labelpath, "w") as fl:
                    fl.write(label)
