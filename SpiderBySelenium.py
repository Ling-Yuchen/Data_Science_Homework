from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep


def main():
    # 创建 WebDriver 对象，指明使用chrome浏览器驱动
    wd = webdriver.Chrome()

    # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
    wd.get('https://wenshu.court.gov.cn/')

    # 设置最大等待时长为 10秒
    wd.implicitly_wait(10)
    sleep(10)

    wd.find_element(By.CLASS_NAME, 'case on').click()
    # wd.find_element(By.ID, 'loginLi').click()

    sleep(2)

    wd.quit()


if __name__ == '__main__':
    main()
