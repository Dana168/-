import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailHelper:
    def __init__(self, host, port, sender, password, receivers, subject, msg, isHtml=False, annexes=None, imges=None):
        super().__init__()
        self.host = host
        self.port = port
        self.sender = sender
        self.password = password
        self.receivers = receivers
        self.subject = subject
        self.msg = msg
        self.isHtml = isHtml
        self.annexes = annexes
        self.imges = imges

    def send(self):
        # 创建根对象
        msgRoot = MIMEMultipart('related2')
        msgRoot['From'] = self.sender
        msgRoot['To'] = ";".join(self.receivers)
        msgRoot['Subject'] = self.subject

        # 创建文本对象
        msgAlternative = MIMEMultipart('alternative2')  #
        msgAlternative.attach(MIMEText(self.msg, 'html' if self.isHtml else 'plain', 'utf-8'))
        msgRoot.attach(msgAlternative)

        # 创建附件对象
        if self.annexes:
            for dict in self.annexes:
                contentBytes = open(dict["filePath"], 'rb').read()
                annex = MIMEText(contentBytes, 'base64', 'utf-8')
                annex["Content-Type"] = 'application/octet-stream'
                annex["Content-Disposition"] = "attachment; filename=" + dict[
                    "fileName"]  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                msgRoot.attach(annex)

        # 创建图片对象
        if self.imges:
            count = 1
            for dict in self.imges:
                file = open(dict["filePath"], 'rb')
                msgImage = MIMEImage(file.read())
                msgImage.add_header('Content-ID', '<image' + str(count) + '>')  # 定义图片 ID，在 HTML 文本中引用
                file.close()
                msgRoot.attach(msgImage)
                count += 1

        # 发送邮件
        try:
            smtpObj = smtplib.SMTP_SSL()
            smtpObj.connect(self.host, self.port)
            smtpObj.login(self.sender, self.password)
            smtpObj.sendmail(self.sender, self.receivers, msgRoot.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件", e)
        pass


if __name__ == '__main__':
    receivers = ["ipython123456@163.com", "ouyangsuo@163.com", "284577461@qq.com"]
    msg = """
    <p>Python 邮件发送测试...</p>
    <p><a href="http://www.baidu.com">百度一下你就知道</a></p>
    <p>图片演示：</p>
    <p><img src="cid:image1"></p>
    <p><img src="cid:image2"></p>
    """
    annexes = [
        {"fileName": "1.txt", "filePath": "../doc/1.txt"},
        {"fileName": "2.txt", "filePath": "../doc/2.txt"},
    ]
    imgs = [
        {"filePath": "../doc/meinvb.jpg"},
        {"filePath": "../doc/china.gif"},
    ]
    mHelper = MailHelper('smtp.qq.com', 465, "2280518818@qq.com", "osdbbzkbspbiaf", receivers, "本邮件来自邮件工具", msg,isHtml=True, annexes=annexes, imges=imgs)
    # mHelper = MailHelper('smtp.qq.com', 465, "2280518818@qq.com", "aafslobwxfdlcacd", receivers, "本邮件来自邮件工具", msg,isHtml=True, annexes=annexes, imges=imgs)
    # mHelper = MailHelper('smtp.qq.com', 465, "2280518818@qq.com", "aafslobwxfdlcacd", receivers, "测试普通邮件",msg)
    mHelper.send()
    pass
