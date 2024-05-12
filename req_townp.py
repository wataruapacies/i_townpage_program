import mysql.connector
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep
import pandas
import random
import urllib.parse
import sys
import os
import urllib.request
from lxml import etree
import datetime
import csv
import shutil


def doing(what,where):
    ua = UserAgent()
    headers = {'user-agent':ua.chrome}

    #print("Good Luck!!")
    box_search_what = what#"病院"#sys.argv[1]
    print(what,where)
    box_search_what_url = urllib.parse.quote(box_search_what)
    box_search_where = where#"大阪府"#sys.argv[2]
    box_search_where_url = urllib.parse.quote(box_search_where)

    csv_file_name = os.path.join('result', box_search_what + '_' + box_search_where + '.csv')
    csv_file_name1 = '/var/www/html/phone_number_app/storage/app/public/python/log/' + box_search_what + '_' + box_search_where + '.csv'
    csv_file_name2 = os.path.join('log', box_search_what + '_' + box_search_where + '.csv')
    cols = ['社名','番号','住所','URL','検索キーワード','検索地域','日時']
    #df = pandas.DataFrame(index=[], columns=cols)
    lista = []
    number_10 = ['0','1','2','3','4','5','6','7','8','9']
    number_p = 0
    get_list = 0
    hitnum_num = 0
    over1000 = False
    while True:
        data_num=0
        #url = "https://itp.ne.jp/keyword?keyword=" + box_search_what_url + "&areaword=" + box_search_where_url + "&sort=01&sbmap=false&area=13&from=" + str(number_p)
        url="https://itp.ne.jp/keyword?areaword="+box_search_where_url+"&from="+str(number_p)+"&keyword="+box_search_what_url+"&sort=01"
        iii = 0
        if number_p > 0:
            if get_list >= hitnum_num:
                break
            if number_p >= hitnum_num:
                break
        sleep(3)
        while True:
            try:
                res = requests.get(url,headers=headers,timeout=20.5)
                break
            except:
                print("next url error")
                print(url)
                sleep(1)
        if number_p == 0:
            while iii < 10:
                iii = iii + 1
                try:
                    xpath = "/html/body/div/div/div[2]/div/div/div/div[2]/div/main/section[3]/div[5]/div[2]/p/span[@class='wixui-rich-text__text']"
                    #        /html/body/div/div/div[2]/div/div/div/div[2]/div/main/section[3]/div[5]/div[2]/p/span
                    
                    soup = BeautifulSoup(res.text,'html.parser')
                    xml = etree.HTML(str(soup))
                    hitnum = xml.xpath(xpath)[0]
                    hitnum_text = hitnum.text
                    print(hitnum_text)
                    print('----------------------')
                    hitnum_text_n=""
                    for jjj in range(len(hitnum_text)):
                        if hitnum_text[jjj] in number_10:
                            hitnum_text_n = hitnum_text_n +hitnum_text[jjj]

                    hitnum_num = int(hitnum_text_n)
                    if hitnum_num >= 1000:
                        hitnum_num = 1000

                    print(hitnum_num)
                    break
                except:
                    print('not found hitnum')
                    print(url)
                    sleep(5)
                    try:
                        res = requests.get(url,headers=headers,timeout=30.5)
                        sleep(5)
                    except:
                        pass
        print(url)
        for i in range(6):
            if hitnum_num ==1000:
                if get_list >= hitnum_num and over1000:
                    print('hitnum last')
                    break
            else:
                if get_list >= hitnum_num:
                    print('hitnum last')
                    break
            kjk = 0
            while kjk<4:
                kjk = kjk + 1
                try:
                    row = ['','','','','','','']
                    xpath="/html/body[@class='responsive']/div/div/div[2]/div/div/div/div[2]/div/main/section[2]/div[2]/div[2]/div[2]/div[2]/div/div[" + str(i+1) + "]/div[3]/div[2]/div[2]/div[4]/p[@class='font_8']/a"
                    #      /html/body/div/div/div[2]/div/div/div/div[2]/div/main/                    section[2]/div[2]/div[2]/div[2]/div[2]/div/div[4]/div[3]/div[2]/div[2]/div[4]/p/a
                    #      /html/body/div/div/div[2]/div/div/div/div[2]/div/main/                    section[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[4]/p/a
                    #      /html/body/div/div/div[2]/div/div/div/div[2]/div/main/section[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div[4]/p/a
                    soup = BeautifulSoup(res.text,'html.parser')
                    xml = etree.HTML(str(soup))
                    company_name = xml.xpath(xpath)[0]
                    row[0]=company_name.text
                    xpath="/html/body[@class='responsive']/div/div/div[2]/div/div/div/div[2]/div/main/section[2]/div[2]/div[2]/div[2]/div[2]/div/div[" + str(i+1) + "]/div[4]/div[4]/div[3]/p/span[@class='wixui-rich-text__text']"
                    #      /html/body/div/div/div[2]/div/div/div/div[2]/div/main/                   section[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[4]/div[4]/div[3]/p/span
                    company_phone = xml.xpath(xpath)[0]
                    phone_number=company_phone.text
                    phone_ans = ""
                    for jjj in range(len(phone_number)):
                        if phone_number[jjj] in number_10:
                            phone_ans = phone_ans +phone_number[jjj]
                    row[1]=phone_ans
                    #print(phone_ans)
                    xpath="/html/body[@class='responsive']/div/div/div[2]/div/div/div/div[2]/div/main/section[2]/div[2]/div[2]/div[2]/div[2]/div/div[" + str(i+1) + "]/div[3]/div[3]/div[2]/div[3]/div[2]/p/span"
                    #      /html/body/div/div/div[2]/div/div/div/div[2]/div/main/                   section[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div[2]/div[3]/div[2]/p/span
                    company_address = xml.xpath(xpath)[0]
                    row[2]=company_address.text
                    #print(company_address.text)
                    xpath="/html/body[@class='responsive']/div/div/div[2]/div/div/div/div[2]/div/main/section[2]/div[2]/div[2]/div[2]/div[2]/div/div[" + str(i+1) + "]/div[3]/div[2]/div[2]/div[4]/p[@class='font_8']/a/@href"
                    url_tmp = xml.xpath(xpath)[0]
                    #print(url_tmp)
                    row[3]=url_tmp
                    row[4]=box_search_what
                    row[5]=box_search_where
                    dt_now=datetime.datetime.now()
                    row[6]=dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
                    # print("row",row)
                    data_num=data_num+1
                    if phone_ans not in lista:
                        lista.append(phone_ans)
    #                    df = df.append(pandas.Series(row, index=df.columns), ignore_index=True)
                        if len(lista)<=1:
                            with open(csv_file_name2, "w", encoding="cp932", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow(cols)
                            with open(csv_file_name2, "a", encoding="cp932", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow(row)
                        else:
                            with open(csv_file_name2, "a", encoding="cp932", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow(row)
                    get_list = get_list + 1
                    break
                except:
                    if get_list >= hitnum_num:
                        print('hitnum last')
                        if hitnum_num == 1000:
                            print('hitnum1000')
                            over1000 = True
                        break
                    if i >= 4:
                        print('for 4 break')
                        break
        for i in range(16):
            if hitnum_num ==1000:
                if get_list >= hitnum_num and over1000:
                    print('hitnum last')
                    break
            else:
                if get_list >= hitnum_num:
                    print('hitnum last')
                    break
            kjk = 0
            while kjk<4:
                kjk = kjk + 1
                try:
                    row = ['','','','','','','']
                    xpath="/html/body[@class='responsive']/div/div/div[2]/div/div/div/div[2]/div/main/section[2]/div[2]/div[2]/div[2]/div[4]/div/div[" + str(i+1) + "]/div[3]/div[2]/div[2]/div[4]/p/a"
                    #      /html/body/div/div/div[2]/div/div/div/div[2]/div/main/                   section[2]/div[2]/div[2]/div[2]/div[4]/div/div[1]/div[3]/div[2]/div[2]/div[4]/p/a
                    soup = BeautifulSoup(res.text,'html.parser')
                    xml = etree.HTML(str(soup))
                    company_name = xml.xpath(xpath)[0]
                    row[0]=company_name.text
                    
                    xpath="/html/body[@class='responsive']/div/div/div[2]/div/div/div/div[2]/div/main/section[2]/div[2]/div[2]/div[2]/div[4]/div/div[" + str(i+1) + "]/div[4]/div[4]/div[3]/p/span"
                    company_phone = xml.xpath(xpath)[0]
                    phone_number=company_phone.text
                    phone_ans = ""
                    for jjj in range(len(phone_number)):
                        if phone_number[jjj] in number_10:
                            phone_ans = phone_ans +phone_number[jjj]
                    row[1]=phone_ans
                    #print(phone_ans)
                    xpath="/html/body[@class='responsive']/div/div/div[2]/div/div/div/div[2]/div/main/section[2]/div[2]/div[2]/div[2]/div[4]/div/div[" + str(i+1) + "]/div[3]/div[3]/div[2]/div[3]/div[3]/p/span[@class='wixui-rich-text__text']"
                    company_address = xml.xpath(xpath)[0]
                    row[2]=company_address.text
                    #print(company_address.text)
                    xpath="/html/body[@class='responsive']/div/div/div[2]/div/div/div/div[2]/div/main/section[2]/div[2]/div[2]/div[2]/div[4]/div/div[" + str(i+1) + "]/div[3]/div[2]/div[2]/div[4]/p/a/@href"
                    url_tmp = xml.xpath(xpath)[0]
                    #print(url_tmp)
                    row[3]=url_tmp
                    row[4]=box_search_what
                    row[5]=box_search_where
                    dt_now=datetime.datetime.now()
                    row[6]=dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
                    data_num=data_num+1
                    if phone_ans not in lista:
                        lista.append(phone_ans)
    #                    df = df.append(pandas.Series(row, index=df.columns), ignore_index=True)
                        if len(lista)<=1:
                            with open(csv_file_name2, "w", encoding="cp932", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow(cols)
                            with open(csv_file_name2, "a", encoding="cp932", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow(row)
                        else:
                            with open(csv_file_name2, "a", encoding="cp932", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow(row)
                    get_list = get_list + 1
                    break
                except:
                    if get_list >= hitnum_num:
                        print('hitnum last')
                        if hitnum_num == 1000:
                            print('hitnum1000')
                            over1000 = True
                        break
                    pass
        number_p = number_p + 20
    #    df.to_csv(csv_file_name1,index=False,encoding="cp932",errors="ignore")
        print(number_p)
        #if number_p>2000:
        #    break
        #if data_num == 0:
        #    break
        if number_p > hitnum_num:
            print('web_last')
            break
        if get_list >= hitnum_num:
            print('web_last getlist')
            break
        sleep(3)
    print("succeed")
    #df.to_csv(csv_file_name,index=False,encoding="cp932",errors="ignore")
    try:
        shutil.copyfile(csv_file_name2, csv_file_name)
    except:
        print('err')
    #sys.stdout.close()
    #sys.stdout = sys.__stdout__
