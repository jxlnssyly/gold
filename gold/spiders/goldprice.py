# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver
import datetime

class GoldpriceSpider(scrapy.Spider):
    name = 'goldprice'
    allowed_domains = ['g-banker.com']
    start_urls = ['https://g-banker.com/']

    def __init__(self):
        self.browser = webdriver.PhantomJS()
        self.price = None

    def parse(self, response):
        # print response.text
        self.browser.get(response.url)
        self.price = float(self.browser.find_element_by_xpath('//*[@id="J_price"]').text)


    def close(self,spider, reason):
        hour = datetime.datetime.now().hour
        if(self.price != None):
            if int(hour) < 22:
                if(self.price > 278):
                    from scrapy.mail import MailSender
                    # mailer = MailSender.from_settings(settings)# 出错了，没找到原因
                    mailer = MailSender(
                        smtphost = "smtp.163.com",  # 发送邮件的服务器
                        mailfrom = "18607970065@163.com",   # 邮件发送者
                        smtpuser = "18607970065@163.com",   # 用户名
                        smtppass = "yan18779865344",  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
                        smtpport = 25   # 端口号
                    )

                    body = u"""
                    实时爬取的黄金价格为:
                    """ + str(self.price)
                    subject = u'爬取的黄金实时价格'
                    # 如果说发送的内容太过简单的话，很可能会被当做垃圾邮件给禁止发送。
                    mailer.send(to=["363918226@qq.com"], subject = subject.encode("utf-8"), body = body.encode("utf-8"))

    def __del__(self):
        self.browser.close()
