import cv2
import mechanize
from bs4 import BeautifulSoup as BS
from captcha import get_text_from_captcha
from captcha import resolve1
import os
import time
import uuid
import glob

from pymongo import MongoClient 
''' 
try: 
    conn = MongoClient('mongodb+srv://ps:M%40r!b0r0@dev-q2lp8.gcp.mongodb.net/test') 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 
'''
# database 
#db = conn.dev1
  
# Created or Switched to collection names: my_gfg_collection 
#collection = db.Car_detail

#os.remove('captcha_img.jpg')

def get_det(vno, collection):
    url = "https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml"
    url_for_captcha = "https://vahan.nic.in/nrservices/cap_img.jsp"

    titles = ["Registration City :", 
                "Registration State :",
                "Registration Number :",
                "Registration Date :",
                "owner Name :",
                "Vehicle Maker :",
                "Vehicle Model :",
                "Vehicle Type :",
                "Fuel Type :",
                "Registration Upto :",
                "MV Tax Upto :",
                "Insurance Upto :",
                "PUCCU Upto :",
                "Emission norms :",
                "RC Status :"]

    results = []
    #main_list = []
    #res_list = []

    br = mechanize.Browser()
    br.set_handle_robots(False)
    
    html = br.open(url)
    soup = BS(html, features="html5lib")
    image_tags = soup.findAll('img')
    imagename = str(uuid.uuid4()) + '.jpg'
    for image in image_tags:
        filename = image['src'].lstrip('http://')
        data = br.open(url_for_captcha).read()
        br.back()
        save = open(imagename, 'wb')
        save.write(data)
        save.close()
    
    #caps = get_text_from_captcha("captcha_img.jpg")
    caps = resolve1(imagename)
    #if len(caps) == 6:
    captchatext = caps
    #else:
        #captchatext = get_text_from_captcha("captcha_img.jpg")
        #print("API Call")
    #captchatext = captchatext.replace(" ", "")
    #print(captchatext)
    captchatext.replace("O", "0")
    text_captcha = str(captchatext).upper()
    print(text_captcha)
    #time.sleep(2)
    br.select_form(name="masterLayout")
    br["regn_no1_exact"] = vno
    br["txt_ALPHA_NUMERIC"] = text_captcha
    res = br.submit()
    content = res.read()
    soup = BS(str(content), features="html5lib")
    prettyHTML = soup.prettify()
    main_list = []
    result = soup.find("div", {"id": "rcDetailsPanel"})
    #print(result)
    if result == None:
        #print(text_captcha)
        return titles, list()
    result = result.prettify()
    
    Authority = soup.find("div",{"class":"font-bold top-space bottom-space text-capitalize"})
    Authority = str(Authority.get_text()).replace("1. Registering Authority: ", "")
    Authority = Authority.replace('  ', '')
    Authority = Authority.replace('\\n', '').replace('\n', '')
    Authority1 = Authority.split(",")
    #print(Authority)

    main_list = []
    for row in soup.findAll("div", {"class":"col-md-3 fit-width-content top-space-5 bottom-space-5 font-bold"}):
        cells = row.get_text()
        text1 = cells.replace('  ', '')
        text2 = text1.replace('\\n', '').replace('\n', '')
        main_list.append(text2)
    #print(main_list)

    main_list1 = []
    for row in soup.findAll("div", {"class":"col-md-3 fit-width-content top-space-5 bottom-space-5"}):
        cells = row.get_text()
        text1 = cells.replace('  ', '')
        text2 = text1.replace('\\n', '').replace('\n', '')
        main_list1.append(text2.strip())
    #print(main_list1)

    owner_list = []
    for row in soup.findAll("div", {"class":"col-md-9 fit-width-content top-space-5 bottom-space-5"}):
        cells = row.get_text()
        text1 = cells.replace('  ', '')
        text2 = text1.replace('\\n', '').replace('\n', '').strip()
        owner_list.append(text2)

    temp = owner_list[1].split("/")
    #print(Place)
    #print(owner_list)
    #print(main_list)
    import pandas as pd
    output = {"Registration City": Authority, 
                "Registration State": Authority1[len(Authority1)-1].strip(),
                "Registration Number": main_list1[0],
                "Registration Date": main_list1[1],
                "owner Name": owner_list[0],
                "Vehicle Maker": temp[0],
                "Vehicle Model": temp[1],
                "Vehicle Type": main_list1[4],
                "Fuel Type": main_list1[5],
                "Registration Upto": main_list1[6],
                "MV Tax Upto": main_list1[7],
                "Insurance Upto": main_list1[8],
                "PUCCU Upto": main_list1[9],
                "Emission norms": main_list1[10],
                "RC Status": main_list1[11]}
    #print(output)
    rec_id1 = collection.insert_one(output)
    results = [Authority,Authority1[len(Authority1)-1].strip(),main_list1[0],main_list1[1],owner_list[0],
              temp[0], temp[1], main_list1[4], main_list1[5], main_list1[6], main_list1[7]
              , main_list1[8], main_list1[9], main_list1[10], main_list1[11]]
    #os.remove(imagename)
    filelist = glob.glob(os.path.join('./', "*.jpg"))
    for f in filelist:
        os.remove(f)

    #print("\n")
    #print("--------------------------------------------")
    #for i in range(len(titles)):
    #    print(titles[i], end=" ")
    #    print(results[i])
    #print("--------------------------------------------")
    
    return titles, results