import urllib.request
from bs4 import BeautifulSoup
import requests
import execjs
import json
from selenium import webdriver
import re
import xlwt


def main():
    askURL("https://wenshu.court.gov.cn/website/parse/rest.q4w")


def askURL(url):
    session = getCookie()
    # 获得已经登录过的session
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    #                          "Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34",
    #            "Cookie": "UM_distinctid=17d7f9e6f07af6-08ba407efcc4df-a7d193d-144000-17d7f9e6f08ae9; "
    #                      "SESSION=7a206c09-49c2-463b-9509-edccfda0a787",
    #            "Referer": "https://wenshu.court.gov.cn/website/wenshu/181107ANFZ0BXSK4/index.html?docId"
    #                       "=e94301637d2c49c5babdadf20106e2e9",
    #            "Accept": "application/json, text/javascript, */*; q=0.01",
    #            }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"}
    html = ""
    # request = urllib.request.Request(url=url, headers=headers,  method='POST')
    # response = urllib.request.urlopen(request)
    # 通过ctx调用js文件的函数
    with open('SpiderHelper.js', encoding='utf-8') as f:
        code = f.read()
    ctx = execjs.compile(code)

    getCipherText = "cipher()".format()
    cipherText = json.loads(ctx.eval(getCipherText))

    getToken = "geneToken('{}')".format(24)
    token = json.loads(ctx.eval(getToken))

    data = {"ciphertext": cipherText, "__RequestVerificationToken": token}

    response = session.post(url=url, headers=headers, data=data)
    html = response.text
    print(html)
    # 打印结果
    getData(html)


def getCookie():
    # 查看网页源码的request headers得到的headers数据
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"}
    loginURL = "https://wenshu.court.gov.cn/website/wenshu/181010CARHS5BS3C/index.html?open=login"
    session = requests.Session()
    # 查看登录时的login的request headers的form data得到的模拟登录的数据
    data = {"username": "17712912271",
            "password": "d0jaf6u7MmlSWzyOvUZxbmmViq09YdsTOJvX1rADH8afQv4OdWSSXkxtx7NGFvsRgEwK4kb"
                        "%2B8rJlb9MQxO8W7J3uTXsebuzo0iaKypMiPxpI2JcarnePg"
                        "%2BHYHxHemC4KrypFYmIrFIJGu699nnu2R7RN1lj1sR8to%2F1CsAqpbb5nAEhcj0s9PbPtsBT6d8qPAtkrqZ3eCcjlw"
                        "%2FnPyrZRMpQMu8wnpe5S44ebNYrMHhLBM7EwzOJIiWkzMQWy6S"
                        "%2FsbaFndzbOWKf0JFuNlJMCa7uLdQmYFoXeBELPKQOsUe3LwYmuoBACDlRZELnNtUeBnu1wA5eS%2FN1DSvZwPYs8sw"
                        "%3D%3D",
            "appDomain": "wenshu.court.gov.cn"}
    # 模拟进行登录，session自动保留的登录的cookie
    response = session.post(url=loginURL, headers=headers, data=data)
    return session


def getData(html):
    bs = BeautifulSoup(html, "html.parser")
    content = ""


if __name__ == '__main__':
    main()
