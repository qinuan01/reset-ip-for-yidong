#仅移动能用
#code by qinuan
from curl_cffi import requests;import base64;import random;from loguru import logger;import time
class res():
    def __init__(self,pwd):
        self.s=requests.Session()
        self.pwd=pwd
        self.s.headers = {'Accept': '*/*','Accept-Language': 'zh-CN,zh;q=0.9','Connection': 'keep-alive','Content-type': 'application/x-www-form-urlencoded','Origin': 'http://192.168.1.1','Referer': 'http://192.168.1.1/html/login_CM.html','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',}
    def check(self):
        self.ip=requests.get('https://httpbin.org/ip').json()['origin']
        logger.debug(self.ip)
    def login(self):
        base64_string = base64.b64encode(self.pwd.encode('utf-8')).decode('utf-8')
        data = {
            'username': 'user',
            'password': base64_string,
            'page': '1',
            'sessionid': self.get_session(),
            'ajaxmethod': 'do_login',
            '_': random.random(),
        }
        response = self.s.post('http://192.168.1.1/cgi-bin/ajax',data=data, verify=False)
        print(response.text)
        print(response)
    def reboot(self):
        data = {
            'sessionid':  self.get_session(),
            'ajaxmethod': 'reboot',
            '_': random.random(),
        }
        response = self.s.post('http://192.168.1.1/cgi-bin/ajax', data=data)
        print(response.text)
        print(response)
    def get_session(self):
        params = {'ajaxmethod': 'get_login_user','_':  random.random(),}
        return self.s.get('http://192.168.1.1/cgi-bin/ajax', params=params,verify=False).json()["sessionid"]
    def run(self):
        self.check()
        self.login()
        try:
            self.reboot()
        except:
            logger.success("重启中")
            time.sleep(5)
        while True:
            try:
                self.check()
                logger.success("重启成功")
                break
            except:
                time.sleep(1)
if __name__ == '__main__':
    your_password=input('输入你的网关密码: ')
  #  your_password=''
    res(your_password).run()
