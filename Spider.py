from bs4 import BeautifulSoup
import urllib.request
import requests
import urllib.error
import re
import xlwt


def main():
    askURL("https://wenshu.court.gov.cn/website/wenshu/181107ANFZ0BXSK4/index.html?docId=cd85419230a14e80b39eadd800c976da")


def askURL(url):
    session = getCookie()
    # 获得已经登录过的session
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"}
    html = ""
    try:
        response = session.get(url=url, headers=headers)
        html = response.text
        print(html)
        # 打印结果
        getData(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


def getCookie():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"}
    loginURL = "https://wenshu.court.gov.cn/website/wenshu/181010CARHS5BS3C/index.html?open=login"
    session = requests.Session()
    data = {"username": "17712912271",
            "password": "d0jaf6u7MmlSWzyOvUZxbmmViq09YdsTOJvX1rADH8afQv4OdWSSXkxtx7NGFvsRgEwK4kb"
                        "%2B8rJlb9MQxO8W7J3uTXsebuzo0iaKypMiPxpI2JcarnePg"
                        "%2BHYHxHemC4KrypFYmIrFIJGu699nnu2R7RN1lj1sR8to%2F1CsAqpbb5nAEhcj0s9PbPtsBT6d8qPAtkrqZ3eCcjlw"
                        "%2FnPyrZRMpQMu8wnpe5S44ebNYrMHhLBM7EwzOJIiWkzMQWy6S"
                        "%2FsbaFndzbOWKf0JFuNlJMCa7uLdQmYFoXeBELPKQOsUe3LwYmuoBACDlRZELnNtUeBnu1wA5eS%2FN1DSvZwPYs8sw"
                        "%3D%3D",
            "appDomain": "wenshu.court.gov.cn"}
    response = session.post(url=loginURL, headers=headers, data=data)
    return session


def getData(html):
    bs = BeautifulSoup(html, "html.parser")
    content = ""


if __name__ == '__main__':
    main()
