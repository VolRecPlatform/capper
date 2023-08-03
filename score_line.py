import requests
import json

# 创建省份id、年份、保留键和存放数据的列表
proid = [11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 50, 51, 52, 53, 54, 61, 62,
        63, 64, 65, 71, 81, 82]
yid = ["2018", "2019", "2020", "2021", "2022"]
keys_to_keep = ["type", "score", "province"]
item_info_update = []

# 创建省份映射字典
province_mapping = {
    "北京": 11,
    "天津": 12,
    "河北": 13,
    "山西": 14,
    "内蒙古": 15,
    "辽宁": 21,
    "吉林": 22,
    "黑龙江": 23,
    "上海": 31,
    "江苏": 32,
    "浙江": 33,
    "安徽": 34,
    "福建": 35,
    "江西": 36,
    "山东": 37,
    "河南": 41,
    "湖北": 42,
    "湖南": 43,
    "广东": 44,
    "广西": 45,
    "海南": 46,
    "重庆": 50,
    "四川": 51,
    "贵州": 52,
    "云南": 53,
    "西藏": 54,
    "陕西": 61,
    "甘肃": 62,
    "青海": 63,
    "宁夏": 64,
    "新疆": 65,
    "台湾": 71,
    "香港": 81,
    "澳门": 82
}

for pid in proid:
    # 不同省份url只在省份id上有差异
    url = 'https://static-data.gaokao.cn/www/2.0/proprovince/{0}/pro.json'.format(pid)
    response = requests.get(url)
    if response.status_code != 200:
        continue
    data = response.json()
    for key in data['data'].keys():
        # 只爬取近五年的数据
        if key not in yid:
            continue
        for category in data['data'][key].keys():
            # 爬取文科、理科、综合、物理类和历史类的数据
            if category != 't_1' and category != 't_2' and category != 't_3' and category != 't_2073' \
                    and category != 't_2074':
                continue
            item_info = data['data'][key][category]
            for i in range(len(item_info)):
                # 许多地区对本科一批分数线的表达有所差异，下面的Unicode将其全部涵盖进去
                if item_info[i]["batch_name"] == "\u672c\u79d1\u4e00\u6279" or \
                        item_info[i]["batch_name"] == "\u672c\u79d1\u6279" or \
                        item_info[i]["batch_name"] == "\u5e73\u884c\u5f55\u53d6\u4e00\u6bb5" or \
                        item_info[i]["batch_name"] == "\u666e\u901a\u7c7b\u4e00\u6bb5" or \
                        item_info[i]["batch_name"] == "\u672c\u79d1\u6279A\u6bb5" or \
                        item_info[i]["batch_name"] == "\u91cd\u70b9\u672c\u79d1\uff08\u6c49\u65cf\uff09" or \
                        item_info[i]["batch_name"] == "\u91cd\u70b9\u672c\u79d1\u6279" or \
                        item_info[i]["batch_name"] == "\u672c\u79d1\u4e00\u6bb5":
                    item_info_dict = {k: v for k, v in item_info[i].items() if k in keys_to_keep}
                    # 在字典中添加年份键以及值
                    item_info_dict['year'] = key
                    # 使用映射字典将中文省份转换为对应的省份ID
                    item_info_dict['province_id'] = province_mapping.get(item_info_dict['province'], None)
                    item_info_update.append(item_info_dict)
# 处理爬取的数据，统一类型
result = []
for item in item_info_update:
    if item['type'] == "1" or item['type'] == "2":
        result.append(item)
    elif item['type'] == "3":
        end_1 = {
            "type": "1",
            "score": item['score'],
            "province": item['province'],
            "year": item['year'],
            "province_id": item['province_id']
        }
        end_2 = {
            "type": "2",
            "score": item['score'],
            "province": item['province'],
            "year": item['year'],
            "province_id": item['province_id']
        }
        result.append(end_1)
        result.append(end_2)
    elif item['type'] == "2073":
        end = {
            "type": "1",
            "score": item['score'],
            "province": item['province'],
            "year": item['year'],
            "province_id": item['province_id']
        }
        result.append(end)
    elif item['type'] == "2074":
        end = {
            "type": "2",
            "score": item['score'],
            "province": item['province'],
            "year": item['year'],
            "province_id": item['province_id']
        }
        result.append(end)
# 将数据写入文件里
with open('score_line.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)
