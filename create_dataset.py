import os
import shutil
from glob import glob
import random
import cv2
from VOCAnnotation import VOCAnnotation


def makedirs(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


images_dir = "dataset1/JPEGImages"
anno_dir = "dataset1/Annotations"
data_list_dir = "dataset1/ImageSets"
makedirs(data_list_dir)

data_list = glob(f"backup/Fires_压缩/train/images/*")

f_train = open(f"{data_list_dir}/train.txt", "w")
f_val = open(f"{data_list_dir}/val.txt", "w")

random.shuffle(data_list)
train_lens = int(len(data_list) * 0.8)
train_list = data_list[:train_lens]
val_list = data_list[train_lens:]


def generate_data(img_path, mode="train"):
    img_name = os.path.basename(img_path)
    target_path = os.path.join(images_dir, mode, img_name)
    makedirs(os.path.dirname(target_path))
    shutil.copyfile(img_path, target_path)
    txt_path = img_path.replace("images", "annotations").replace("jpg", "txt")
    with open(txt_path, "r") as f:
        data = f.readlines()

    img = cv2.imread(img_path)
    voc = VOCAnnotation(img_name, img.shape[1], img.shape[0])
    for item in data:
        item = item.split()
        name = item[1]
        xmin, ymin, xmax, ymax = [int(i) for i in item[2:]]

        voc.addBoundingBox(xmin, ymin, xmax, ymax, name)
    xml_path = os.path.join(anno_dir, mode, img_name.replace("jpg", "xml"))
    makedirs(os.path.dirname(xml_path))
    voc.save(xml_path)
    log = f"../JPEGImages/{mode}/{img_name} ../Annotations/{mode}/{img_name.replace('jpg', 'xml')}"
    return log


for img_path in train_list:
    log = generate_data(img_path)
    f_train.write(log + "\n")

for img_path in val_list:
    log = generate_data(img_path, "val")
    f_val.write(log + "\n")

