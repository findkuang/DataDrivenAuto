#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/20 21:23
# @Author  : kuangxiaojiang
# @File    : EmailHandler.py
# @Function:
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from Utils.LoggerHandler import logger


class EmailHandler(object):

    def read_report(self):
        f = open(r'C:\Users\Aisonk\PycharmProjects\seenew\reportname.html', 'rb')
        return f.read()

    def send_email(self):
        """ 发送邮件 """

        # 第三方 SMTP 服务
        mail_host = "smtp.163.com"  # 设置服务器
        mail_user = "findkuang@163.com"  # 用户名
        mail_pass = "Kxj123456a"  # 口令
        # 获取口令地址 https://www.cnblogs.com/zhangshan33/p/11943755.html

        # 设置收件人和发件人
        sender = 'findkuang@163.com'
        receivers = ['1027872612@qq.com', '2919923219@qq.com', 'findkuang@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        # 创建一个带附件的实例对象
        message = MIMEMultipart()

        # 邮件主题、收件人、发件人
        subject = '请查阅--测试报告'  # 邮件主题
        message['Subject'] = Header(subject, 'utf-8')
        # message['From'] = Header("{}".format(sender), 'utf-8')  # 发件人
        message['To'] = Header("{}".format(';'.join(receivers)), 'utf-8')  # 收件人
        message['From'] = 'findkuang@163.com'  # 发件人
        # message['To'] = 'findkuang@163.com'  # 收件人

        # 邮件正文内容 html 形式邮件
        send_content = self.read_report()  # 获取测试报告
        html = MIMEText(_text=send_content, _subtype='html', _charset='utf-8')  # 第一个参数为邮件内容

        # 构造附件
        att = MIMEText(_text=send_content, _subtype='base64', _charset='utf-8')
        att["Content-Type"] = 'application/octet-stream'
        file_name = 'report.html'
        att["Content-Disposition"] = 'attachment; filename="{}"'.format(file_name)  # # filename 为邮件附件中显示什么名字
        message.attach(html)
        message.attach(att)
        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtp_obj.login(mail_user, mail_pass)
            smtp_obj.sendmail(sender, receivers, message.as_string())
            smtp_obj.quit()
            logger('发送邮件').debug("邮件发送成功！")
        except smtplib.SMTPException:
            logger('发送邮件').error("Error: 无法发送邮件！")


if __name__ == '__main__':
    email = EmailHandler()
    email.send_email()