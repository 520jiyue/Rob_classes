"""
新凯里学院官网
"""
import execjs                    # 用来执行js脚本
import requests                  # 用来请求网页，获取网页内容
from bs4 import BeautifulSoup    # 用来解析网页内容
import csv                       # 用来写入csv文件
import re                        # 用来匹配内容
import time                      # 用来延时
import ddddocr                   # 用来识别验证码
import os                        # 用来判断文件是否存在

def one_sleep():
    time.sleep(1)

index_url = "http://sys.kluniv.edu.cn:8003"
session = requests.session()

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 "
                  "Safari/537.36 Edg/121.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Cookie": "_gscu_670124149=805331319upx0619; _ga=GA1.1.202793893.1685956507; "
                       "_ga_QYKCGTHFGK=GS1.1.1685956507.1.1.1685956952.0.0.0; "
                       "ASP.NET_SessionId=sekouqhtdlhnftj0rzj5ezwe",
    "Host": "sys.kluniv.edu.cn:8003",
}

resp = session.get(index_url, headers=header)
print(resp.status_code)
soup = BeautifulSoup(resp.text, 'lxml')
viewState = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
public_key_exponent = soup.find('input', attrs={'name': 'txtKeyExponent'})['value']
public_key_modulus = soup.find('input', attrs={'name': 'txtKeyModulus'})['value']
img_url = soup.find('img', attrs={'id': 'icode'})['src']
SafeKey = img_url.split("=")[-1]
yzm_url = soup.find()
user_id = ""
password = ""

# print(img_url)

# js逆向 textbox2
with open("rea.js", "r", encoding="utf-8") as file:
    result = file.read()
    file.close()
js = execjs.compile(result)
TextBox2 = js.call("password_ase", public_key_exponent, public_key_modulus, password)


# 发送请求 获取图片
img_url_total = index_url + img_url
# print(img_url_total)
data_img = {
    "SafeKey": SafeKey
}
resp_img = session.get(img_url_total, headers=header, stream=True, data=data_img)
print(resp_img.status_code)
with open(r'yzm.jpg', 'wb') as f:
    f.write(resp_img.content)
f.close()


# 识别验证码 识别之前以防图片还没有下载完成 判断文件是否存在 不存在时休眠1s
while not os.path.exists("yzm.jpg"):
    one_sleep()
ocr = ddddocr.DdddOcr()

with open('yzm.jpg', 'rb') as f:
    img_bytes = f.read()

yzm = ocr.classification(img_bytes)




data = {
  "__VIEWSTATE": viewState,
  "__VIEWSTATEGENERATOR": "9BD98A7D",
  "txtUserName": user_id,
  "TextBox2": TextBox2,
  "txtSecretCode": yzm,
  "RadioButtonList1": "学生",
  "Button1": "登录",
  "txtKeyExponent": "010001",
  "txtKeyModulus": public_key_modulus
}
# print(data)
_resp = session.post(index_url, headers=header, data=data)
login_data = {
    "xh": user_id
}
login_resp = session.get(index_url + f"/xs_main.aspx?xh={user_id}", headers=header, data=login_data)
print(login_resp.status_code)
print(login_resp.text)


resp.close()
login_resp.close()
