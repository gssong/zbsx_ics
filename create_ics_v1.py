# /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
now = datetime.now().strftime('%Y%m%dT%H:%M:%S')

import re
import httpx  # httpx与requests的api相似，可以仅更改httpx为requests，代码运行无误
from faker import Faker  # 设置伪造请求头user-agent
from lxml import etree
def get_url(url):
    #headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'zh-CN,zh;q=0.9','Connection': 'keep-alive','User-Agent': Faker().chrome(version_from=98, version_to=100, build_from=4800, build_to=5000),}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    try:
        response = httpx.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        return None

def set_ics_header():
    # year为当前年份
    return "BEGIN:VCALENDAR\n" \
           + "PRODID:NULL\n" \
           + "VERSION:2.0\n" \
           + "CALSCALE:GREGORIAN\n" \
           + "METHOD:PUBLISH\n" \
           + f"X-WR-CALNAME:闸北实验小学菜单\n" \
           + "X-WR-TIMEZONE:Asia/Shanghai\n" \
           + f"X-WR-CALDESC:闸北实验小学菜单\n" \
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


def parse_html(html):
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


def concat_ics(y):  # 返回一个完整的ics文件内容
    header = set_ics_header(y)



def save_ics(fname, text):
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(text)

url = 'http://www.syxx.edu.sh.cn/info/iList.jsp?cat_id=10020'
fname = r'D:\calendar_2023_cd.ics'
text = set_ics_header()+ parse_html(get_url(url)) + 'END:VCALENDAR'
save_ics(fname,text)


