from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


def main():
    spider('https://anli.court.gov.cn/static/web/index.html#/alk/list')


def spider(web):
    # 创建 WebDriver 对象，指明使用chrome浏览器驱动
    wd = webdriver.Chrome()

    # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
    wd.get(web)

    # 设置最大等待时长为 10秒
    wd.implicitly_wait(10)

    # 进入此页面的第一个case
    wd.find_element(By.CSS_SELECTOR, 'body .ul_list li .li_h').click()

    # 从这一份开始爬取 爬取100份
    for i in range(100):
        wd = spiderByCase(wd, i + 1)

    wd.quit()


# 爬取这个页面上的案例，rank为这个案例的序号
def spiderByCase(wd, rank):
    # 等待页面刷新
    sleep(1)

    # 找到所有文本的内容
    fullText = wd.find_elements(By.CSS_SELECTOR, '.caseDetailContent #content .text p')

    # 定位到“裁判结果”，并保存之后的第二个webElement, 用flag标识是否遇到了“裁判结果”
    flag = 0
    content = ""
    for paragraph in fullText:
        # 遇到了裁判结果栏目
        if paragraph.text == "裁判结果":
            flag = 1
        else:
            # 刚刚遇到这个栏目 需要经过一个空隙
            if flag == 1:
                flag += 1
            # 到达文本内容
            elif flag == 2:
                content = paragraph.text
                break

    write(content, rank)

    # 进入上一篇
    wd.find_element(By.CSS_SELECTOR, 'body .prev').click()

    return wd


# 将content写入txt
def write(content, rank):
    path = 'res/' + str(rank) + '.txt'
    f = open(path, 'w', encoding='utf-8')
    f.write(content)
    f.close()


if __name__ == '__main__':
    main()
