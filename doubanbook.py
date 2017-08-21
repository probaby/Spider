import requests
import re

response = requests.get("https://book.douban.com")
text = response.text
#print(text)
#str = '<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>'
str2 = '<li.*?cover.*?<a href="(.*?)".*?title="(.*?)".*?more-meta.*?class="author">(.*?)</span>.*?class="year">(.*?)</span>'

pattern = re.compile(str2,re.S)
a = re.findall(pattern,text)
#print(a)
for value in a:
    print(value)
