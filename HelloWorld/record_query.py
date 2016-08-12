# -*- coding: utf-8 -*-
__author__ = 'lizhihui'
'''
使用Python 3.5的urllib库实现爬虫技术
我可是玩300英雄的男人 我将通过该例子爬取我游戏中的角色信息
'''
import urllib.request as ur
import re
import pandas as pd  # 利用大数据知识将最终数据整理成DataFrame格式 方便查看


# 获取数据的方法
def getData(name):
    # 设置请求头 Request Headers 我在这用的是360浏览器8.1 请求头需要设置的信息打开网页按F12选择Network 查看就好了
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/45.0.2454.101 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Accept-Language': 'zh-CN,zh;q=0.8'}  # 我在这就设置两个属性 user_agent代表请求身份
    # 填写要爬取数据的网址 利用quote函数将中文字符转换为url编码(百分比编码)
    request = ur.Request('http://300report.jumpw.com/list.html?name=' + ur.quote(name), headers=headers)
    response = ur.urlopen(request).read()  # read()函数返回的是bytes类型数据
    z_response = response.decode('UTF-8')  # 将返回数据设置为UTF-8编码
    # print(z_response)
    # *************************判断是否查询到角色信息**************************************************

    if z_response.find('请输入角色名称') >= 0:
        return '没有查询到该角色的战绩哦/:?\n难不成是手抖输错角色名了?/:dig'

    # *************************利用正则表达式开始对返回数据进行处理************************************

    data1 = ['角色名', '角色等级', '节操值', '总胜场', '总场次', '更新日期']  # 爬取角色基本数据的数据索引
    data2 = ['最受欢迎玩家', '常胜王排行', '重度玩家排行', '团队实力排行']  # 爬取角色服务器排名的数据索引
    roleInfo = []  # 爬取的角色数据将暂时存放于此

    for data in data1:
        # 将正则表达式编译成Pattern对象
        pattern = re.compile(data + r':.*</td>', re.I)  # re.I:不区分大小写模式
        # 开始匹配 未匹配到数据返回None
        result = re.search(pattern, z_response)
        '''
           # 使用match()函数匹配 注意:match()函数必须在0位置匹配成功才有返回
           result = re.match(pattern, z_response)  # 未匹配到数据返回None
           # 使用search()函数匹配 注意:search方法与match方法极其类似，区别在于match()函数只检测re是不是在string的开始位置匹配，search()会扫描整个string查找匹配
           result = re.search(pattern, z_response) # 未匹配到数据返回None
           # 以列表形式返回全部能匹配的子串
           result = re.findall(pattern, z_response)

           注意:1.match()及search()函数都只能匹配到第一个结果
                  两个函数一旦匹配到结果会里面终止匹配,然后返回匹配结果
                  想返回多个结果请使用findall()函数
                2.未匹配到数据调用group()函数会报错,错误信息:AttributeError: 'NoneType' object has no attribute 'group'
        '''
        if not result:  # result为None 匹配失败
            print('未匹配到数据')
        else:  # 匹配成功
            # print(result.group())
            # 开始对匹配到的字符串进行切割处理
            s = result.group()[result.group().index(':'):]
            info = s[s.index('<td>') + 4:-5]  # 利用切片对字符串进行截取
            roleInfo.append(info)  # 追加元素到roleInfo列表中

    # 开始统计胜利及失败场数
    result1 = re.findall(r'胜利', z_response)
    win = len(result1)  # 胜利场数
    failure = 10 - win  # 失败场数

    # 开始统计竞技场跟战场胜利数
    result_zc = re.findall(r'战场', z_response)
    zc = len(result_zc)  # 战场数
    jjc = 10 - zc  # 竞技场数

    '''
    # 两个list合并成一个dict,用于展示最终角色数据
    # roleInfos = dict(zip(data1, roleInfo))
    '''
    print('\n小爬虫爬取到的的数据:\n', roleInfo)
    # 将最终数据整理成DataFrame格式 方便查看
    data = pd.Series(roleInfo, index=data1)
    print('\n整理后的数据:\n', data)
    # 输出胜利及失败场数
    print('\n最近10场战绩:', '%d胜 %d负\n' % (win, failure))

    return '最近10场战绩:'+'%d胜%d负\n其中玩了%d把战场,%d把竞技场' % (win, failure, zc, jjc)