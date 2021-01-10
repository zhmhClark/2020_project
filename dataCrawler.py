#返回一个字典，格式为{'语言名称1':{'日期1':'百分比1','日期2':'百分比2',...},'语言名称2':{'日期1':'百分比1','日期2':'百分比2',...},}
import requests
from bs4 import BeautifulSoup
import re
class TiobeData():
    def __init__(self):
        self.data = {}
        self.url = "https://www.tiobe.com/tiobe-index/"

    def GetData(self):
        req = requests.get(self.url)#设置爬取地址
        req.encoding = "utf-8"#设置爬取到的文档编码格式为utf-8
        result=''.join(re.findall(r'series: (.*?)\}\);',req.text,re.DOTALL))#获取html文档中编程语言排名的数据
        result = re.findall(r'({.*?})', result, re.DOTALL)#对爬取到的数据中的转译字符取消
        tiobedata = {}#准备一个空字典
        for item in result:#遍历得到的数据
            name = ''.join(re.findall(r"{name : '(.*?)'", item, re.DOTALL))#得到一个语言的名字
            data = re.findall(r"\[Date.UTC(.*?)\]", item, re.DOTALL)#得到对应语言一系列的时间与相应时间下的使用比率
            time_value ={}#准备存放时间与使用比率的数据
            for i in data:#遍历对应语言的一系列的时间与相应时间下的使用比率
                i = i.replace(' ', '')#删除某个时间与相应时间下的使用比率的数据中的空格
                i = re.sub(r'[()]', '', i)#获取更为精简的字符串
                value = i.split(',')[-1]#获取时间
                time_list = i.split(',')[:3]#获取使用比率
                time = ""
                for index, j in enumerate(time_list):#将获取到的时间格式化
                    if index !=0:
                        if len(j) == 1:
                            j = '0' + j
                    if index == 0:
                        time += j
                    else:
                        time += '-' + j
                time_value.update({time:value})#添加时间——比率的字典
            tiobedata.update({name:time_value})#为返回的字典添加数据
        return tiobedata#返回有格式为{'语言名称1':{'日期1':'百分比1','日期2':'百分比2',...},'语言名称2':{'日期1':'百分比1','日期2':'百分比2',...},}的字典