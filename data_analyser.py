import json


def analyse_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    img_list = data['images']
    annotations = data['annotations']
    categories = data['categories']

    img_id_set = set()
    for ann in annotations:
        img_id = ann['image_id']
        img_id_set.add(img_id)

    print(categories)
    print(len(img_list), len(img_id_set))


if __name__ == '__main__':
    json_file = '/home/gaoxin/data/train_val/jyz_pl_v2/coco/annotations/instances_val2017.json'
    analyse_data(json_file)