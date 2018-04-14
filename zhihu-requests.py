# -*- coding:UTF-8 -*-

import requests, time
import hmac, json
from bs4 import BeautifulSoup
from hashlib import sha1


# def get_captcha(data, need_cap):
#     ''' 处理验证码 '''
#     if need_cap is False:
#         return
#     with open('captcha.gif', 'wb') as fb:
#         fb.write(data)
#     return input('captcha:')


def get_signature(grantType, clientId, source, timestamp):
    ''' 处理签名 '''

    hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', None, sha1) # 这个数字在js中查找
    hm.update(str.encode(grantType)) # 括号中是转为字节  这几个的顺序
    hm.update(str.encode(clientId))
    hm.update(str.encode(source))
    hm.update(str.encode(timestamp))
    print(str(hm.hexdigest()))
    return str(hm.hexdigest())


def login(username, password, s,header):
    ''' 处理登录 '''
    # resp1 = s.get('https://www.zhihu.com/signin', headers=headers)  # 这个是登录页面，里面有_xsrf
    # print(resp1.text)
    # resp2 = s.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=cn', headers=header)  # 拿cookie:capsion_ticket
    # need_cap = json.loads(resp2.text)["show_captcha"]  # {"show_captcha":false} 表示不用验证码
    # print("=========================================")
    # print(resp2.text) # {"show_captcha":false} 此处不在进行验证码验证，这个是判断是否有验证码的
    grantType = 'password'
    clientId = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    timestamp = str(int(time.time()*1000))
    # resp1 = s.get('https://www.zhihu.com/signin', headers=headers)  # 这个是登录页面，里面有_xsrf
    # print(resp1.text)
    resp2 = s.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=cn', headers=header) # 拿cookie:capsion_ticket
    # captcha = json.loads(resp2.text)["show_captcha"]  # {"show_captcha":false} 表示不用验证码
    data = {
        "client_id": clientId,
        "grant_type": grantType,
        "timestamp": timestamp,
        "source": source,
        "signature": get_signature(grantType, clientId, source, timestamp),  # 获取签名
        "username": username,
        "password": password,
        "lang": "cn",
        "captcha": "",  # 获取图片验证码
        "ref_source": "homepage",
        "utm_source": ""
    }

    print("=========: " + str(data))
    print("-" * 50)
    resp = s.post('https://www.zhihu.com/api/v3/oauth/sign_in', data, headers=headers).text
    print(resp)
    print("-" * 50)
    return resp


if __name__ == "__main__":
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
               'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
               "Referer":"https://www.zhihu.com/signup?next=%2F"
               # 通过看headers中的数据，可以把感觉有用的都加上
               }

    login('18339180716', '891068920.com', session, headers)  # 用户名密码换自己的就好了
    resp = session.get('https://www.zhihu.com/inbox', headers=headers)  # 登录进去了，可以看私信了
    print(BeautifulSoup(resp.content, 'html.parser'))
    print(resp.cookies.items())
    print(resp.cookies)
