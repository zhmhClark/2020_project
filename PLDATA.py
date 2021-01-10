# *_*coding: UTF-8*_*
# 开发人员   : LENOVO
# 开发时间   : 2021/1/3 11:57
# 文件名称   : lx2.PY
# 开发工具   : PyCharm
import warnings
import numpy as np
import matplotlib.pyplot as plt
##################################################################################################################################################
#调用另一个文件夹里的TiobeData 要讲两个文件放到同一个工程里
from dataCrawler import TiobeData
TbData= TiobeData()
data1=TbData.GetData()
#################################################################################################################################################
# 将含有小数的数字字符串转换为数字
def numberstr2num(num_str):
    '''
    能完美处理整数小数字符串转数字的算法
    :param num_str:
    :return:
    '''
    import re
    assert isinstance(num_str, str)
    if num_str and re.match('(-|\\+)?\\d+(\\.\\d+)?', num_str):
        capital_char = num_str[0]
        if capital_char == '-' or capital_char == '+':
            num_str = num_str[1:]
        segs = num_str.split('.')
        # 整数部分字符串
        num_seg = segs[0]
        # 得到整数部分数值
        total_num = str2num(num_seg)
        # 存在小数部分字符串
        if len(segs) == 2:
            point_num_seg = segs[1]
            # 加上小数部分数值
            total_num += pointstr2num(point_num_seg)

        return total_num if not capital_char == '-' else 0 - total_num
def str2num(num_str):
    # 主方法已经验证过数字有效性，这里就不必再验证了
    index = 0
    str_len = len(num_str)
    num = 0
    for c in num_str:
        index += 1
        num += (ord(c) - 48) * pow(10, str_len - index)
    return num


def pointstr2num(point_str):
    # 主方法已经验证过数字有效性，这里就不必再验证了
    index = 0
    point_num = 0
    for c in point_str:
        index += 1
        point_num += (ord(c) - 48) / pow(10, index)
    return point_num

sz=[] ##总共的日期
for i in data1['C'].keys():
    sz.append(i)
#print(sz)


names=[]
for k in data1.keys():
    names.append(k)
#['C', 'Java', 'Python', 'C++', 'C#', 'Visual Basic', 'JavaScript', 'PHP', 'R', 'SQL']
#######################################################################################################################
#二维字典操作函数 需要更改二维字典到合适的样子
def addtwodimdict(thedict, key_a, key_b, val):
  if key_a in thedict.keys():
    thedict[key_a].update({key_b: val})
  else:
    thedict.update({key_a:{key_b: val}})

#kay_a是日期 kay_b是names val 是函数
data2=dict()
for k1 in data1.keys():
  for k2 in data1[k1].keys():
   addtwodimdict(data2,k2,k1,numberstr2num(data1[k1][k2]))#通过键可以直接得到值

print(data2.keys())
##################################################################################################################
#填补空缺
temp=1
temp_k=0
for k3 in data2.keys():
  length= len(data2[k3].keys())
  if length>temp:
     temp=length
     temp_k=k3
#print(temp,temp_k)
for k4 in data2.keys():
    length2=len(data2[k4].keys())
    if length2<temp:
       for k5 in data2[temp_k].keys():
           if k5 not in data2[k4].keys():
               data2[k4].update({k5: 0})
colors = ['k', 'r', 'sienna', 'yellow', 'g', 'aquamarine', 'dodgerblue', 'pink', 'b', 'darkviolet']
#names = ['C', 'Java', 'Python', 'C++', 'C#', 'Visual Basic', 'JavaScript', 'PHP', 'R', 'Groovy']##所有的names
color_dict = {'Java':'k','C++':'r', 'Groovy':'sienna', 'Visual Basic':'yellow', 'Python':"g",'JavaScript':'aquamarine', 'R':'dodgerblue','C':'pink','C#':'b','PHP':"darkviolet"}
from collections import OrderedDict
##################################################################################################################
#按日期进行排序
def sort_key(old_dict, reverse=False):
  # 对字典按key排序, 默认升序, 不修改原先字典
    # 先获得排序后的key列表
    keys = sorted(old_dict.keys(), reverse=reverse)
    # 创建一个新的空字典
    new_dict = OrderedDict()
    # 遍历 key 列表
    for key in keys:
        new_dict[key] = old_dict[key]
    return new_dict
data2=sort_key(data2)
print(data2)
print(len(data2))
##################################################################################################################
#进行绘图操作
ax = plt.gca()
for data_item in data2.items():
    plt.cla()
    temp = sorted(data_item[1].items(), key=lambda item: item[1])
    x = [item[0] for item in temp]
    color = [color_dict[i] for i in x]
    y = [item[1] for item in temp]
    plt.barh(range(1, 11), y, color=color)
    plt.title(data_item[0], fontproperties='simhei', fontsize=24)

    plt.yticks(range(1, 11),
               list(x),
               fontproperties='simhei', fontsize=16
               )
    plt.xticks(range(0, 30, 100))
    for x, y in zip(range(1, 11), y):
        plt.text(y + 0.1, x - 0.1, str(y))
    plt.pause(0.006)
plt.show()



