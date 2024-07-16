import requests as req
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import openpyxl 

###############################
#開啟XLSX
wb1 = openpyxl.Workbook()
#TABLE 0
sheet = wb1.worksheets[0]
###############################


def CJK_cleaner(string): 
    #filters = re.compile(u'[^0-9a-zA-Z\u4e00-\u9fff]+', re.UNICODE)
    filters = re.compile('[^0-9a-zA-Z\u4e00-\u9fff\uFF00-\uFFEF\u3000-\u303F\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65]+', re.UNICODE)
    return filters.sub('', string)

def CJK_LIST(list):
    list = [ CJK_cleaner(i.text) for i in list ]
    return list
  
def cookie_split(cookie):
    cookies = {}
    for line in cookie.split(";"):
      if line.find("=") != -1:
          name,value = line.strip().split("=", 1)
          cookies[name] = value
    return cookies
  
from Title_name import dict_ru_sell

def TITLE(choise,sheet):
    TITLE=[]

    for i in choise:
        print(i)
        TITLE.append(dict_ru_sell.get(f"t{i}")) 
        print(TITLE)
    sheet.append(TITLE)

def OUTPUT(td,choise,n):

    if len(choise)>1:

        ans=(CJK_LIST(td[choise[0]:n:10]),)
        for i in choise[1:]: 
            ans=ans+(CJK_LIST(td[i:n:10]),)
        OUTPUTs=list(zip(*ans))

    return OUTPUTs

    
#your cookie
'''from fake_useragent import UserAgent
ua = UserAgent()'''
cookie='YOUR COOKIE'

#cookie split
cookies=cookie_split(cookie)

#Your User-agent
headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/XXX.XX (KHTML, like Gecko) Chrome/XXX.X.0.0 Safari/XXX.XX'}

#user SET
choise=[1,2,3,5]
TITLE(choise,sheet)

#catch
for i in range(99):
    finish="{0}".format(i)
    print(finish)
    url="https://mybid.ruten.com.tw/master/my.php?l_type=buy_full&p={0}".format(i)
    res=req.get(url,cookies=cookies,timeout = 10,headers=headers)
    res.encoding=res.apparent_encoding
    html=res.text
    soup=BeautifulSoup(html,features="lxml")
    n=len(soup.tbody.select('td'))
    td=soup.tbody.select('td')
    if (n ==0):
        break

    OUTPUTs=OUTPUT(td,choise,n)                  #per page OUTPUT

    for row in OUTPUTs:
        if "已取消交易" in row or "逾期取消" in row :
            continue
        sheet.append(row)

##SAVE
wb1.save('new.xlsx')
