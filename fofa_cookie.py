import requests
import base64
import re
import time
from lxml import etree

headers1 = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Cookie": ""
}


def fofa_web_search(search_keyword, page, save_route):
    url = 'https://fofa.info/result?qbase64='
    search_data_bs = base64.b64encode(search_keyword.encode('utf-8')).decode('utf-8')
    for p in range(1, (page + 1)):
        page_new = '&page={}&page_size=10'.format(p)
        urls = url + search_data_bs + page_new
        try:
            result = requests.get(urls, headers=headers1).content.decode('utf-8')
            html = etree.HTML(result)
            ip_data = html.xpath('//a[@target="_blank"]/@href')
            ip_data_new = '\n'.join(set(ip_data))
            with open(save_route, mode='a+') as fp:
                fp.write(ip_data_new + '\n')
                fp.close()
            time.sleep(0.5)
        except Exception as e:
            time.sleep(0.5)
            pass


def fofa_host_search(search_keyword, page, save_route, mode_ip):
    url = 'https://fofa.info/result?qbase64='
    search_data_bs = base64.b64encode(search_keyword.encode('utf-8')).decode('utf-8')
    for p in range(1, (page + 1)):
        page_new = '&page={}&page_size=10'.format(p)
        urls = url + search_data_bs + page_new
        try:
            result = requests.get(urls, headers=headers1).content.decode('utf-8')
            pattern = r',Array\(10\),(.*),{'
            result_ip = re.search(pattern, result)
            ip_data = result_ip.group(1)
            if mode_ip:
                ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
            else:
                ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}')
            ips = re.findall(ip_pattern, ip_data)
            for ip in ips:
                with open(save_route, mode='a+') as fp:
                    fp.write(ip + '\n')
            time.sleep(0.5)
        except Exception as e:
            time.sleep(0.5)
            pass


if __name__ == '__main__':
    #搜索关键字
    search_keyword = '"proftpd" && country="DE" && port="2"'
    #获取的页数
    page = 100
    #保存文件地址
    save_route = "result.txt"
    #false是保存ip:port,true是只保存ip
    mode_ip = False
    #fofa_web_search(search_keyword, page, save_route)
    fofa_host_search(search_keyword, page, save_route, mode_ip)
