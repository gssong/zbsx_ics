# /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
now = datetime.now().strftime('%Y%m%dT%H:%M:%S')

import re
#import httpx  # httpx与requests的api相似，可以仅更改httpx为requests，代码运行无误
import requests
from lxml import etree
def get_url(url):
    #headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'zh-CN,zh;q=0.9','Connection': 'keep-alive','User-Agent': Faker().chrome(version_from=98, version_to=100, build_from=4800, build_to=5000),}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        return None

def set_ics_header():
    # 构建ics头部信息
    return "BEGIN:VCALENDAR\n" \
           + "PRODID:NULL\n" \
           + "VERSION:2.0\n" \
           + "CALSCALE:GREGORIAN\n" \
           + "METHOD:PUBLISH\n" \
           + f"X-WR-CALNAME:闸北实验小学\n" \
           + "X-WR-TIMEZONE:Asia/Shanghai\n" \
           + f"X-WR-CALDESC:闸北实验小学\n" \
           + "BEGIN:VTIMEZONE\n" \
           + "TZID:Asia/Shanghai\n" \
           + "X-LIC-LOCATION:Asia/Shanghai\n" \
           + "BEGIN:STANDARD\n" \
           + "TZOFFSETFROM:+0800\n" \
           + "TZOFFSETTO:+0800\n" \
           + "TZNAME:CST\n" \
           + "DTSTART:19700101T000000\n" \
           + "END:STANDARD\n" \
           + "END:VTIMEZONE\n"


def set_item_ics(item, date, uid):  # item: 菜名，date：日期，uid：编序
    if '休息' in item:
        return "BEGIN:VEVENT\n" \
               + f"DTSTART;VALUE=DATE:{date}\n" \
               + f"DTEND;VALUE=DATE:{date}\n" \
               + f"DTSTAMP:{date}T000001\n" \
               + f"UID:{date}T{uid:0>6}_jr\n" \
               + f"CREATED:{date}T000001\n" \
               + f"DESCRIPTION:{item}\n" \
               + f"LAST-MODIFIED:{now}\n" \
               + "SEQUENCE:0\n" \
               + "STATUS:CONFIRMED\n" \
               + f"SUMMARY:{item}\n" \
               + "TRANSP:TRANSPARENT\n" \
               + "END:VEVENT\n"
    else:
        return "BEGIN:VEVENT\n" \
               + f"DTSTAMP:{date}T000001\n" \
               + f"UID:{date}T{uid:0>6}_jr\n" \
               + f"DTEND;TZID=Asia/Shanghai:{date}T123000\n" \
               + f"TRANSP:OPAQUE\n" \
               + f"CREATED:{date}T000001\n" \
               + f"DESCRIPTION:{item}\n" \
               + f"LAST-MODIFIED:{now}\n" \
               + f"DTSTART;TZID=Asia/Shanghai:{date}T120000\n" \
               + "SEQUENCE:1\n" \
               + "STATUS:CONFIRMED\n" \
               + f"SUMMARY:{item}\n" \
               + "TRANSP:TRANSPARENT\n" \
               + "END:VEVENT\n"


def parse_html_menu(html):
    html = etree.HTML(html)
    text = ''
    for i in range(15):
        d = html.xpath('//*[@id="body"]/div/div[2]/div[2]/div[2]/a['+str(i+1)+']/p/text()')
        a = html.xpath('//*[@id="body"]/div/div[2]/div[2]/div[2]/a['+str(i+1)+']')

        newstitle= re.sub(r'\n','',d[0])
        newstitle = re.sub(r' +', '', newstitle)
        if '学生菜谱' in newstitle:
            #print(newstitle)
            cpurl = 'http://www.syxx.edu.sh.cn'+a[0].attrib.get('href')
            text = text + getmenu(get_url(cpurl))
    return text

def ft(c):
    c = re.sub('\s','',c)
    c = re.sub(r'\n','',c)
    return c

def getmenu(url):
    m = etree.HTML(url)
    year = m.xpath('//*[@id="body"]/div/div[2]/div/div[2]/div[1]/p[2]/u/span/text()')[0]
    text = ''
    for i in range(7):
        try:
            date = m.xpath('//*[@id="body"]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr['+str(i+2)+']/td[1]/p/span/text()')[0].split('/')
            cai = m.xpath('//*[@id="body"]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr['+str(i+2)+']/td[3]/p/span/text()')[0]
            tang = m.xpath('//*[@id="body"]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr['+str(i+2)+']/td[4]/p/span/text()')[0]
            date =datetime(int(year),int(date[0]),int(date[1]))
            d = date.strftime("%Y%m%d")
            c = ft(cai)
            t = ft(tang)
            if c!= '':
                print(d,c+t)
                text = text + set_item_ics(c+t, d, 1)



        except:
            pass
    return text


def concat_ics():  # 返回一个完整的ics文件内容
    return set_ics_header()+ parse_html_menu(get_url(url)) + set_item_course() + 'END:VCALENDAR'

def set_item_ics_course(date, course, start_t,end_t,uid):
    return "BEGIN:VEVENT\n" \
           + f"DTSTAMP:{date}T000001\n" \
           + f"UID:{date}T{uid:0>6}_jr\n" \
           + f"DTEND;TZID=Asia/Shanghai:{date}T{end_t}\n" \
           + f"TRANSP:OPAQUE\n" \
           + f"CREATED:{date}T000001\n" \
           + f"DESCRIPTION:{course}\n" \
           + f"LAST-MODIFIED:{now}\n" \
           + f"DTSTART;TZID=Asia/Shanghai:{date}T{start_t}\n" \
           + "SEQUENCE:1\n" \
           + "STATUS:CONFIRMED\n" \
           + f"SUMMARY:{course}\n" \
           + "TRANSP:TRANSPARENT\n" \
           + "END:VEVENT\n"




def set_item_course():
    text = ''
    # 这是一个字典，键是星期几，值是那天的课程列表
    course_schedule = {
        1: ["班队会, 自然, 信息, 数学", "语文, 体育, 道法"],
        2: ["语文, 体育, 数学, 唱游", "自然, 语文, 写字"],
        3: ["体综, 美术, 语文, 语文", "英语, 唱游, 探究"],
        4: ["语文, 数学, 体育, 英语", "语文, 道法, 美术"],
        5: ["语文, 体育, 开口说时政, 小主综", "小主综","语文, 体育, 动手做数学, 小主综"]
    }
    time_schedule = {
        0: ["082000", "113000"],
        1: ["130000", "162000"],
        2: ["130000", "134000"]
    }
    import datetime

    # 假设的节假日列表, 根据需要自行修改
    holidays = [
        datetime.date(2023, 9, 29),  # 中秋
        datetime.date(2023, 10, 2),  #
        datetime.date(2023, 10, 3),  #
        datetime.date(2023, 10, 4),  #
        datetime.date(2023, 10, 5),  #
        datetime.date(2023, 10, 6),  #
        datetime.date(2024, 1, 1),  #
        # 其他节假日...
    ]

    specialworkdays = {
        datetime.date(2023, 10, 7): 4,
        datetime.date(2023, 10, 8): 5
    }
    # 设置开始和结束日期
    start_date = datetime.date(2023, 9, 1)
    end_date = datetime.date(2024, 1, 19)

    # 生成日期列表
    date_list = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    # 过滤掉周末和法定节假日
    working_days = [date for date in date_list if
                    (date.weekday() not in [5, 6] or date in specialworkdays.keys()) and date not in holidays]

    # 以列表形式打印出工作日
    #print([day.strftime("%Y%m%d") for day in working_days])
    for day in working_days:
        if day in specialworkdays.keys():
            week = specialworkdays[day]
        else:
            week = day.weekday() + 1
        weekn = day.isocalendar()[1] % 2  # 判断单双周
        print(day.strftime("%Y%m%d"), week, weekn)
        #上午课程
        if week == 5 and weekn == 1:
            courses = course_schedule[week][2]
        else:
            courses = course_schedule[week][0]
        print(courses,time_schedule[0])
        text = text + set_item_ics_course(day.strftime("%Y%m%d"),courses,time_schedule[0][0],time_schedule[0][1],2)
        #下午课程
        if week == 5:
            time_afternoon = time_schedule[2]
        else:
            time_afternoon = time_schedule[1]
        print(course_schedule[week][1],time_afternoon)
        text = text + set_item_ics_course(day.strftime("%Y%m%d"),course_schedule[week][1],time_afternoon[0],time_afternoon[1],3)
    return text



def save_ics(fname, text):
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(text)

url = 'http://www.syxx.edu.sh.cn/info/iList.jsp?cat_id=10020'
fname = 'calendar_2023_cd.ics'
text = concat_ics()
save_ics(fname,text)


