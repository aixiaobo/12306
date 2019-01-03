from splinter.browser import Browser
from time import sleep
import traceback
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header


# 实现自动购票的类
class Buy_Tickets(object):
    # 定义实例属性，初始化
    def __init__(self, username, passwd, order, passengers, dtime, starts, ends):
        self.username = username
        self.passwd = passwd
        self.order = order     # 车次，0代表所有车次
        self.passengers = passengers      # 乘客名
        self.starts = starts     # 起始地和终点
        self.ends = ends
        self.dtime = dtime    # 日期
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initMy_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.driver_name = 'chrome'
        self.executable_path = 'C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe'

    # 登录功能实现
    def login(self):
        self.driver.visit(self.login_url)
        self.driver.fill('loginUserDTO.user_name', self.username)
        # sleep(1)
        self.driver.fill('userDTO.password', self.passwd)
        # sleep(1)
        print('请输入验证码...')
        while True:
            if self.driver.url != self.initMy_url:
                sleep(1)
            else:
                break

    def sendMail(self, mail_title, mail_content):
        my_sender = 'xxx@qq.com'  # 发件人邮箱账号
        my_user = 'xxxx@qq.com'  # 收件人邮箱账号
        try:
            '''发送邮件'''
            msg = MIMEText(mail_content, "plain", 'utf-8')  # 发送邮件内容
            msg["Subject"] = Header(mail_title, 'utf-8')  # 发送邮件主题/标题
            msg["From"] = formataddr(['Bruce pk', my_sender])  # 邮件发送方
            msg["To"] = formataddr(['brucepk', my_user])  # 邮件接收方

            s = smtplib.SMTP("smtp.qq.com", 25)  # 邮箱的传输协议，端口默认25
            s.login(my_sender, 'xxxxx')  # 登录邮箱，这里的第二个参数为qq邮箱授权码，不要填你的登录密码
            s.sendmail(my_sender, [my_user, ], msg.as_string())  # 发送方，接收方，发送消息
            s.quit()  # 退出邮箱
            print("抢票通知邮件发送成功！")
        except Exception:
            print("邮件发送失败~~")

    # 买票功能实现
    def start_buy(self):
        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        # 窗口大小的操作
        self.driver.driver.set_window_size(1200, 700)
        self.login()
        self.driver.visit(self.ticket_url)
        try:
            print('开始购票...')
            # 加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
            self.driver.reload()
            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        self.driver.find_by_text('预订')[self.order - 1].click()
                        sleep(1.5)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        for i in self.driver.find_by_text('预订'):
                            i.click()
                            sleep(1)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            print('开始预订...')
            sleep(1)
            print('开始选择用户...')
            for p in self.passengers:
                self.driver.find_by_text(p).last.click()
                sleep(0.5)
                if p[-1] == ')':
                    self.driver.find_by_id('dialog_xsertcj_ok').click()
            sleep(3)
            print('提交订单...')
            self.driver.find_by_id('submitOrder_id').click()
            sleep(5)
            print('确认选座...')
            self.driver.find_by_id('qr_submit_id').click()
            print('预订成功...')
            sleep(5)
            self.sendMail(mail_title, mail_content)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    username = 'xxxx'    # 用户名
    password = 'xxxx'    # 密码
    order = 0       # 车次选择，0代表所有车次
    # 乘客名，比如 passengers = ['XXX', 'XXX']
    # 学生票需注明，注明方式为：passengers = ['XXX(学生)', 'XXX']
    passengers = ['gengzhiboy']
    # 日期，格式为：'2019-01-28'
    dtime = '2019-01-28'
    # 出发地(需填写cookie值)
    starts = '%u4E0A%u6D77%2CAOH'  # 上海  %u4E0A%u6D77%2CAOH  上海南 %u4E0A%u6D77%u5357%2CSNH
    # 目的地(需填写cookie值)
    ends = '%u5E7F%u5DDE%2CIZQ'  # 广州  %u5E7F%u5DDE%2CIZQ   北京  %u5317%u4EAC%2CBJP
    mail_title = '抢票成功！赶紧去支付！！'   # 邮件标题
    mail_content = '抢票成功了！赶紧去支付！！抢票成功了！赶紧去支付！！'  # 邮件内容
    Buy_Tickets(username, password, order, passengers, dtime, starts, ends).start_buy()

