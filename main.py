import os
import json
from datetime import datetime


# 获取文件地址，这里是在py文件所在目录下的json_files文件夹下
def get_file_loc(file_name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__)) + '\\json_files/'
    return current_dir + file_name


# 获取json文件并转化为字典
def get_json_dic(file_loc: str) -> dict:
    with open(file_loc) as json_file:
        return json.load(json_file)


# 组装最长字典，即所有字段组合出来的一个对象，正好能对应一个完整的表头，第二个参数是key转化的名字，也就是你想转化出来的id字段
def get_dict_longest(json_dic: dict, obj_name: str = '') -> dict:
    attr_list = {}
    if obj_name != '':
        attr_list[obj_name] = ''
    for dic_key, dic_val in json_dic.items():
        attr_list |= dic_val
    for key in list(attr_list):
        attr_list[key] = None  # 对字典的每一个字段赋值为空
    return attr_list


# 另一种写法，把没见过的字段加进列表attr_list中，但是这样写待会儿还得从列表组装字典，所以这个函数就没用到
def get_attr_list(json_dic: dict, obj_name: str = '') -> list:
    attr_list = []
    if obj_name != '':
        attr_list.append(obj_name)
    for dic_key, dic_val in json_dic.items():
        for attr in list(dic_val):
            if attr not in attr_list:
                attr_list.append(attr)
    return attr_list


# 根据最长字典做字段填充解析并生成关系化的数据
def parse_dict_bibliography(json_dic: dict, attr_list: dict, obj_name: str = '') -> list:
    par_dict = []
    has_obj_name = True
    if obj_name not in attr_list:
        has_obj_name = False
    for dic_key, dic_val in json_dic.items():
        item = attr_list.copy()  # 这里调用copy()的原因是因为需要对该对象做一个深拷贝，不用copy()就会拷贝指针从而修改原对象attr_list
        if has_obj_name:
            item[obj_name] = dic_key
        for key, val in dic_val.items():
            item[key] = val
        par_dict.append(item)
    return par_dict


# 对提供的字段做切分并生成一个并集列表，也即是所有关键词的集合
def split_attr_list(json_dic: dict, attr_key: str, split_key: str) -> list:
    parse_list = []
    for dic_key, dic_val in json_dic.items():
        items: list = dic_val[attr_key].split(split_key)
        for item in items:
            data: str = item.lstrip().rstrip()  # 去掉头尾空格
            if data not in parse_list:
                parse_list.append(data)
    parse_list.sort()  # 这里调用了排序，也可以不排序，不排序生成的数据就会和count_keywords_list函数生成数据的顺序一样，只是缺少了个数统计
    return parse_list


# 统计出有哪些key并生成一个key : number字典来计数，之所以不在上面的函数中一下子写完就是为了解耦合，方便不同的数据提取和函数复用
def count_keywords_dict(json_dic: dict, attr_key: str = 'keywords', split_key: str = ',') -> dict:
    key_num_dict = {}
    for dic_key, dic_val in json_dic.items():
        items: list = dic_val[attr_key].split(split_key)
        for item in items:
            data: str = item.lstrip().rstrip()  # 去掉头尾空格
            if data not in key_num_dict:
                key_num_dict[data] = 1
            else:
                key_num_dict[data] += 1
    key_num_dict_str = {}
    for key, val in key_num_dict.items():
        key_num_dict_str[key] = str(val)
    return key_num_dict_str


# 统计出有哪些key并生成一个key : number字典来计数，之所以不在上面的函数中一下子写完就是为了解耦合，方便不同的数据提取和函数复用
def count_keywords_list(json_dic: dict, attr_key: str = 'keywords', split_key: str = ',', key_name: str = 'keyword',
                        val_num: str = 'count') -> list:
    key_num_dict = {}
    for dic_key, dic_val in json_dic.items():
        items: list = dic_val[attr_key].split(split_key)
        for item in items:
            data: str = item.lstrip().rstrip()  # 去掉头尾空格
            if data not in key_num_dict:
                key_num_dict[data] = 1
            else:
                key_num_dict[data] += 1
    key_num_dict_str = []
    for key, val in key_num_dict.items():
        key_item = {key_name: key, val_num: str(val)}
        key_num_dict_str.append(key_item)
    return key_num_dict_str


# 获取每个对象名（'id'）和对应的keyword_list
def get_keyword_list(json_dic: dict, attr_key: str = 'keywords', obj_name: str = '', split_key: str = ',') -> list:
    keyword_list = []
    has_obj_name = True
    if obj_name == '':
        has_obj_name = False
    for dic_key, dic_val in json_dic.items():
        item = {}
        if has_obj_name:
            item[obj_name] = dic_key
        for key in dic_val[attr_key].split(split_key):
            data: str = key.lstrip().rstrip()  # 去掉头尾空格
            item[data] = 1
        keyword_list.append(item)
    return keyword_list


# 获取每个对象名（'id'）和对应的keyword_list，只不过是关系化的形式
def get_keyword_list_format(json_dic: dict, format_list: list, attr_key: str = 'keywords', obj_name: str = '',
                            split_key: str = ','):
    keyword_list = []
    keyword_list


# attr_list里面放的是获取的关键字头，也就是"keywords"切分后的列表
def parse_dict_keywords(json_dic: dict, attr_list: dict, key_attr: str = '') -> list:
    parse_dict = []
    for dic_key, dic_val in json_dic.items():
        item = attr_list.copy()
        for key, val in dic_val.items():
            item[key]


# 对象存为json文件
def dict_to_json(par_dic: list, file_loc: str) -> bool:
    with open(file_loc, 'w') as json_file:
        json.dump(par_dic, json_file, indent=4)
    return os.path.exists(file_loc)


# 打印运行结果
def print_run_info(result: bool, source_behaviour: str, target_behaviour: str, is_datetime_open: bool):
    print_str = ''
    if result:
        print_str += 'Succeeded'
    else:
        print_str += 'Failed'
    print_str += ' run ' + source_behaviour + ' to ' + target_behaviour
    if is_datetime_open:
        print_str += ' in ' + str(datetime.today())
    print(print_str)


if __name__ == '__main__':
    json_dic = get_json_dic(get_file_loc('bibliography.json'))
    # 生成主数据
    if dict_to_json(parse_dict_bibliography(json_dic, get_dict_longest(json_dic, 'id'), 'id'),
                    get_file_loc('bibliography_modified.json')):
        print_run_info(True, 'source file', 'target file', True)
    else:
        print_run_info(False, 'source file', 'target file', True)
    # 生成key统计字段
    if dict_to_json(count_keywords_list(json_dic, 'keywords', ','), get_file_loc('count_keywords.json')):
        print_run_info(True, 'source data', 'statistical data', True)
    else:
        print_run_info(False, 'source data', 'statistical data', True)

    # 生成key并集
    if dict_to_json(split_attr_list(json_dic, 'keywords', ','), get_file_loc('split_attr_list.json')):
        print_run_info(True, 'source attribute', 'target attribute', True)
    else:
        print_run_info(False, 'source attribute', 'target attribute', True)
    # 生成keyword_list
    if dict_to_json(get_keyword_list(json_dic, 'keywords', 'id', ','), get_file_loc('keyword_list.json')):
        print_run_info(True, 'keywords', 'list', True)
    else:
        print_run_info(False, 'keywords', 'list', True)
