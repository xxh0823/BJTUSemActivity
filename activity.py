import requests
import re
import time
import smtplib #加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
my_sender='xxxxxxxx@bjtu.edu.cn'
#这里改为你发邮件的信箱，建议为学校的邮件，因为发邮件需联网，校内网还是很不错的。
my_user=('xxxxxxxxx@qq.com','xxxxxxxxx@qq.com','xxxxxx@bjtu.edu.cn')
#这里是收邮件的信箱，逗号后面可以继续添加多个进行群发。

def mail():
    ret=True
    try:
        msg=MIMEText(' 点击链接预约吧，这是活动预报的网址哦 "http://sem.bjtu.edu.cn/lists-sem_hdyb.html" ','plain','utf-8')
        msg['From']=formataddr(["畅畅",my_sender])  #括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = ",".join(my_user) #括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="有新的信息变动" #邮件的主题，也可以说是标题
        #server=smtplib.SMTP("smtp.163.com",25)
        server=smtplib.SMTP("mail.bjtu.edu.cn",25) #发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender,"********")  #括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,my_user,msg.as_string())  #括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  #这句是关闭连接的意思
    except Exception:  #如果try中的语句没有执行，则会执行下面的ret=False
        ret=False
    return ret
def change():
    ret=mail()
    shi=time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
    if ret:
        print("ok") #如果发送成功则会返回ok
        print(shi)
    else:
        print("filed") #如果发送失败则会返回filed
        print(shi)

while True:
    try:
        print("正在监控")
        url="http://sem.bjtu.edu.cn/lists-sem_hdyb.html"
        kv={'user-agent':'Mozilla/5.0'}
        kv1={'user-agent':'Chrome/59.0.3071.104'}
        r=requests.get(url,headers=kv)
        title=re.findall(r'<span class="tit_em1">(.*?)</span>',r.text,re.S)#活动标题
        link=re.findall(r'href="(.*?)" class="tit_em mb20',r.text)#活动链接
        old = []
        for i in range(len(title)):
            old.append(str(title[i]) + str(link[i]))

        time.sleep(3)

        g=requests.get(url,headers=kv1)
        title2=re.findall(r'<span class="tit_em1">(.*?)</span>',g.text,re.S)
        link2=re.findall(r'href="(.*?)" class="tit_em mb20',g.text)
        new = []
        for i in range(len(title)):
            new.append(str(title2[i]) + str(link2[i]))
        if old != new:
            newTitle = set(new) - set(old)
            print(newTitle)
            if '前沿讲座' in str(newTitle) or '素质拓展' in str(newTitle):
                change()
                # break
    except Exception as e:
        print(e)
        print(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time())))
