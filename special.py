# -*- coding = utf-8 -*-
"""
# @Time :2023/7/24 14:15
# @Author:wjj
"""
import requests
import json
import re


# 定义处理空格的函数
def remove_spaces(input_string):
    return input_string.replace(' ', '').replace('\n', '').replace('\t', '')


# 定义处理双引号的函数
def handle(object):
    s = remove_spaces(object["spname"])
    # 使用正则表达式找到被双引号包围的部分
    matches = re.findall(r'\".*?\"', s)
    # 计算'"'的个数
    count = s.count('"')

    if count % 2 == 0:
        if len(matches) == 1:
            s = s.replace(matches[0], '“' + matches[0][1:-1] + '”')
        if len(matches) == 2:
            s = s.replace(matches[0], '“' + matches[0][1:-1] + '”')
            s = s.replace(matches[1], '“' + matches[0][1:-1] + '”')
        if len(matches) == 3:
            s = s.replace(matches[0], '“' + matches[0][1:-1] + '”')
            s = s.replace(matches[1], '“' + matches[0][1:-1] + '”')
            s = s.replace(matches[2], '“' + matches[0][1:-1] + '”')
        object["spname"] = s
    else:
        # 为奇数，直接置空
        object["spname"] = "null"
    return object


# 各学校各专业遍历
# 创建一个保存把最终数据写入到文件的列表out_to_file
out_to_file = []
# 设置计数器，记录爬取学校的数量
flag = 0
# proid为我国34个省对应id的列表
proid = [11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 50, 51, 52, 53, 54, 61, 62,
        63, 64, 65, 71, 81, 82]
# 设置字典中需要保留的字段
keys_to_keep = ['school_id', 'type', 'province', 'max', 'min', 'min_section', 'level1_name', 'spe_id', 'spname',
                'local_batch_name']
# 近五年年份
year_id = ['2018', '2019', '2020', '2021', '2022']
# 利用三重循环来遍历我国的3000多所高校（sid代表学校id）在34个省，近五年（yid代表年份）的收分数据
for sid in range(30, 3681):
    for pid in proid:
        for yid in year_id:
            # url根据年份、省份、学校代号的不同，会返回相应学校的json文件
            url = "https://static-data.gaokao.cn/www/2.0/schoolspecialscore/{0}/{1}/{2}.json".format(sid, yid, pid)
            response = requests.get(url)
            # item_info用于存爬取到的所有数据
            item_info = []
            # item_info_update用于存筛选后的数据
            item_info_update = []
            # 查看状态码是否为200ok
            if response.status_code != 200:
                continue
            data = response.json()
            # 根据json结构找到需要的数据
            for key in data['data'].keys():
                item_info = data['data'][key]['item']
                item_info_update = [{} for _ in item_info]
                # 遍历列表item_info中包含的字典
                for i in range(len(item_info)):
                    for key in item_info[i].keys():
                        # 删除不需要的键
                        if key not in keys_to_keep:
                            continue
                        item_info_update[i][key] = item_info[i].get(key, 'null')
                    # 在这里添加对应的年份键值对
                    item_info_update[i]['year'] = yid
                # 将处理后的数据都添加到out_to_file里
                out_to_file.extend(item_info_update)
    flag += 1
    print(flag)

# 脏数据清洗
result = [handle(object) for object in out_to_file]

# 将处理后的result转换为json
out_to_file = json.dumps(result, indent=4)
# 将Unicode编码转换为中文
out_to_file = out_to_file.encode('utf-8').decode('unicode_escape')
# 写入到本地文件中
with open("score_special.json", 'w', encoding='utf-8') as f:
    f.write(out_to_file)
