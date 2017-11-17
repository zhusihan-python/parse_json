#coding:utf-8
"""
Created on 2017-11-15
@author jtsh12@163.com
"""


import csv


def list_level(lis):
"""
 this function to find the depth level of input list
"""
    level = 0
    for ele in lis:
        if ele == '':
            level +=1
        else:
            return level
    return level


def parse_to_json(file_path):
"""
 this func parse the csv and split each row into different part according to its depth level
 and combine them into json string
"""
    try:
        csvfile = open(file_path, 'r', encoding='utf-8')
        reader = csv.reader(csvfile)
        
        result = {}

        for row in reader:
            if 0 == list_level(row):
                root_key = row[0]
                outer_key = row[1]
                inner_key = row[2]
                inner_value = row[3:]
                result[root_key] = [{outer_key:[{inner_key:inner_value}]}]
            elif 1 == list_level(row):
                outer_key = row[1]
                inner_key = row[2]
                inner_value = row[3:]
                result[root_key].append({outer_key:[{inner_key:inner_value}]})
            elif 2 == list_level(row):
                inner_key = row[2]
                inner_value = row[3:]
                for item in result[root_key]:
                    if outer_key in item.keys():
                        item[outer_key].append({inner_key:inner_value})
            elif 3 == list_level(row):
                inner_value = row[3:]
                for item in result[root_key]:
                    if outer_key in item.keys():
                        for inner_item in item[outer_key]:
                            if inner_key in inner_item.keys():
                                inner_item[inner_key].extend(inner_value)
            else:
                pass
    finally:
        csvfile.close()
        return result


class Node(object):
"""
 define a container aims to store dict key and previous item
 we can find the full path of a item in the json easier
"""
    def __init__(self, key, value, level=0, prev=None):
        self.level = level
        self.prev = prev
        self.key = key
        self.value = value
        

def split_dict(json_dict, level=0, prev=None):
"""
 split the json_dict and store them in Node recursively
"""
    if isinstance(json_dict, dict):
        dict_key = list(json_dict.keys())[0]
        dict_value = json_dict[dict_key]
        Nodes.append(Node(level=level, key=dict_key, value=dict_value, prev=prev))

        if [node for node in Nodes if node.level<=level]:
            pre_level_node = sorted([node for node in Nodes if node.level<=level], key=lambda x:x.level)[-1]
        else:
            pre_level_node = Nodes[0]

        for ele in dict_value:
            split_dict(ele, level=level+1, prev=pre_level_node)


def find(key):
"""
 find if the key in Nodes then return the full path else return not found
"""    
    path = []
    for node in Nodes:
        if key == node.key:
            while node.prev != None:
                path.append(node.key)
                node = node.prev
            # add the root node key
            path.append(node.key)
            return '.'.join(path[::-1])
        elif key in node.value:
            path.append(key)
            while node.prev != None:
                path.append(node.key)
                node = node.prev
            path.append(node.key)
            return '.'.join(path[::-1])
    return '不存在关键字：{}'.format(key)
       

if __name__ == '__main__':
    result = parse_to_json('history.csv')
    print(result)
    Nodes = []
    split_dict(result)
    path1 = find('欧洲')
    print(path1)
    path2 = find('美洲')
    print(path2)
    path3 = find('金字塔')
    print(path3)