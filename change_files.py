import os
import shutil
import xml.etree.ElementTree as ET
import cv2


def indent(elem,level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def change_files(img_path, xml_path, txt_file, start_num, out_img_path, out_xml_path, out_txt_file):
    if not os.path.exists(out_img_path):
        os.makedirs(out_img_path)
    if not os.path.exists(out_xml_path):
        os.makedirs(out_xml_path)
    img_file_list = []
    with open(txt_file, 'r', encoding='utf-8') as f:
        data = f.readlines()
        for line in data:
            line = line.rstrip()
            file_name = os.path.basename(line)
            img_file_list.append(file_name)
    with open(out_txt_file, 'w', encoding='utf-8') as f:
        for i in range(len(img_file_list)):
            file_name = img_file_list[i]
            out_img_name = str(i + start_num) + '.jpg'
            src_file = os.path.join(img_path, file_name + '.jpg')
            dst_file = os.path.join(out_img_path, out_img_name)
            if os.path.exists(src_file):
                shutil.copy(src_file, dst_file)
            else:
                src_file = os.path.join(img_path, file_name + '.JPG')
                shutil.copy(src_file, dst_file)

            xml_file = os.path.join(xml_path, file_name + '.xml')
            xml_out_file = os.path.join(out_xml_path, str(i + start_num) + '.xml')
            if os.path.exists(xml_file):
                tree = ET.parse(xml_file)
                root = tree.getroot()
                root.find('filename').text = out_img_name
                root.find('path').text = out_img_name
                tree.write(xml_out_file, encoding="utf-8")  # , xml_declaration=True)
            else:
                root = ET.Element('annotation')  # 创建节点
                tree = ET.ElementTree(root)  # 创建文档

                # 图片文件上一级目录
                folder = ET.Element("folder")
                folder.text = ''
                root.append(folder)

                # 文件名
                filename = ET.Element('filename')
                filename.text = out_img_name
                root.append(filename)

                # 路径
                path = ET.Element("path")
                path.text = out_img_name
                root.append(path)

                # source
                source = ET.Element("source")
                root.append(source)
                database = ET.Element("database")
                database.text = "Unknown"
                source.append(database)

                # size
                img = cv2.imread(dst_file)
                h, w, c = img.shape
                size = ET.Element("size")
                root.append(size)
                width = ET.Element("width")  # 宽
                width.text = str(w)
                size.append(width)
                height = ET.Element("height")  # 高
                height.text = str(h)
                size.append(height)
                depth = ET.Element("depth")  # 深度
                depth.text = str(c)
                size.append(depth)

                # segmented
                segmented = ET.Element("segmented")
                segmented.text = str(0)
                root.append(segmented)

                indent(root, 0)
                tree.write(xml_out_file, encoding="utf-8")  # , xml_declaration=True)

            f.write(str(i + start_num) + '\n')

    return len(img_file_list)


if __name__ == '__main__':
    img_path = '/home/gaoxin/data/train_val/jyz_pl/images'
    xml_path = '/home/gaoxin/data/train_val/jyz_pl/xml'
    txt_file = '/home/gaoxin/data/train_val/jyz_pl/val_voc.txt'
    start_num = 0
    out_img_path = '/home/gaoxin/data/train_val/jyz_pl/coco/val2017'
    out_xml_path = '/home/gaoxin/data/train_val/jyz_pl/coco/xml'
    out_txt_file = '/home/gaoxin/data/train_val/jyz_pl/coco/val_voc.txt'
    start_num = change_files(img_path, xml_path, txt_file, start_num, out_img_path, out_xml_path, out_txt_file)

    img_path = '/home/gaoxin/data/train_val/jyz_pl/images'
    xml_path = '/home/gaoxin/data/train_val/jyz_pl/xml'
    txt_file = '/home/gaoxin/data/train_val/jyz_pl/train_voc.txt'
    out_img_path = '/home/gaoxin/data/train_val/jyz_pl/coco/train2017'
    out_xml_path = '/home/gaoxin/data/train_val/jyz_pl/coco/xml'
    out_txt_file = '/home/gaoxin/data/train_val/jyz_pl/coco/train_voc.txt'
    change_files(img_path, xml_path, txt_file, start_num, out_img_path, out_xml_path, out_txt_file)
