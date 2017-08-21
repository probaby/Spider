import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
import codecs

def get_one_page(url):
    try:
        response= requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern, html);
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }

def write_to_file(content):
    #,encoding='utf-8'
    #decode('utf-8', 'ignore')
    #如果没有codecs.open,直接用open回产生 乱码
    with codecs.open('d://result.txt','+a',encoding='utf-8') as f :
        j = json.dumps(content,ensure_ascii=False)+'\n'
        f.write(j)
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        #print(item)
        write_to_file(item)
    
if __name__ == '__main__':
    #不使用进程池时
#    for i in range(10):
#        main(i*10)
# 使用线程池得到的顺序不一定
        pool = Pool()
        pool.map(main,[i*10 for i in range(10)])
    