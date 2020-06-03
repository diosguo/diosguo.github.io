import os 
import time 
import re
import shutil

post_header = """---
layout: post
title: '{}'
subtitle: '{}'
date: {}
categories: {}
author: 迪奥斯郭
cover: '{}'
tags: {}
---
"""

base_dir = './raw_documents'

def get_document_time_str(md_path) -> str:
    modify_time = os.path.getmtime(md_path)
    modify_time = time.localtime(modify_time)
    return time.strftime("%Y-%m-%d", modify_time)


def copy_image_file(source_path, target_path):
    target_path = '.'+target_path
    path = os.path.split(target_path)[0]
    if not os.path.exists(path):
        print(path)
        print(target_path)
        os.makedirs(path)
    shutil.copyfile(os.path.join(base_dir,source_path), target_path)


def get_image_path(image_path):
    image_path = re.findall(r'!\[.*?\]\((.*?)\)$', image_path.strip())[0]
    new_filename = '/assets/blog_img/{}'.format(image_path)
    return image_path, new_filename


def replace_image_path_in_line(line:str) -> str:
    image_path = re.findall(r'!\[(.*?)\]\((.*?)\)$', line.strip())
    if image_path:
        # exist image
        image_path = image_path[0]
        old_image, new_image = get_image_path(line)
        copy_image_file(old_image, new_image)
        # {{"/assets/blog_img/2019-07-23-EM算法.assets/20170521183913_G2ZRf.jpeg" | absolute_url}}){:height="200"}
        new_line = '![{}]({{{{"{}" | absolute_url}}}}){{:height="200"}}'.format(image_path[0], new_image)
        return new_line
    else:
        return line

def convert_one_document(md_path:str):
    filename = os.path.split(md_path)[-1][:-3]
    time_str = get_document_time_str(md_path)
    converted_filename = '{}-{}.md'.format(time_str, filename)
    print(converted_filename)

    tags = ['subtitle','categories','cover','tags']    
    tags_data = {}
    tag_mode = 4
    
    with open(os.path.join('./_posts/',converted_filename), 'w', encoding='utf8') as fou:
        with open(md_path,'r', encoding='utf8') as fin:
            for line in fin:
                if tag_mode:
                    line = line.strip()
                    if line == '':
                        continue
                    tag_mode -= 1
                    line_splited = line.split(' ',1)
                    if line_splited[0] in ['subtitle','categories','tags']:
                        tags_data[line_splited[0]] = line_splited[1]
                    if line_splited[0] == 'cover':
                        old_image, new_image = get_image_path(line)
                        copy_image_file(old_image, new_image)
                        tags_data['cover'] = new_image
                    if tag_mode == 0:
                        header_str = post_header.format(filename, tags_data['subtitle'], time_str, tags_data['categories'], tags_data['cover'], tags_data['tags'])
                        fou.write(header_str+'\n')
                else:
                    new_line = replace_image_path_in_line(line)
                    fou.write(new_line+'\n')
    
                
    print(header_str)
    


def main():
    filepath = './raw_documents/一点思考.md'
    
    convert_one_document(filepath)



if __name__ == "__main__":
    main()