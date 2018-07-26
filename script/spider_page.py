#!/usr/bin/env python
# coding=utf-8
__author__ = 'wagyou'

import hashlib
import time
import urllib
import urllib2
import json
import sys
import traceback
import ssl
import gzip
import StringIO

default_request_headers = {
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Cache-Control": "max-age=0",
        "Cookie": "BIDUPSID=1203860230980E85AC98667D08312C26; PSTM=1482392671; BAIDUID=ACF8E733595D3C2417E63A9320C07340:FG=1; MCITY=-131%3A; BAIDUCUID=08vDi0a6280s8Hisl8HR80ut2ug1uHaGjOSgujul-t8ou28pgaBgi_aHv8jRa2fHA; plus_cv=1::m:f3b912ac; plus_lsv=cac6b919a188c590; video_wise=d19d778e8237c406; attention=cb3dc18046d80e10; PSINO=2; H_PS_PSSID=1428_21111;"}
MAX_RETRY_TIMES = 3

class PageSpider():
    def __init__(self, headers = default_request_headers, max_retry_times = MAX_RETRY_TIMES, timeout = 3, sleep_time = 1):
        self.__headers = headers
        self.__max_retry_times = max_retry_times
        self.__timeout = timeout
        self.__sleep_time = sleep_time

    def crawl_page(self, url):
        for i in range(0, self.__max_retry_times):
            try:
                req = urllib2.Request(url, headers=self.__headers)
                response = urllib2.urlopen(req, data=None, timeout=self.__timeout, context=ssl._create_unverified_context())
                if response.info().get('Content-Encoding') == 'gzip':
                    response = gzip.GzipFile(fileobj = StringIO.StringIO(response.read()))
                post_res_str = response.read()
                return post_res_str
            except:
                print >>sys.stderr, "crawl [%s] fail" % url
                traceback.print_exc(file=sys.stderr)
                time.sleep(self.__sleep_time)
        return None

if __name__ == "__main__":
    ps = PageSpider()
    for line in sys.stdin:
        line = line.strip("\r\n")
        sps = line.split("\t")
        ret = ps.crawl_page(sps[0])
        if ret != None:
            print "%s\t%s" % (sps[0], ret.replace("\r", " ").replace("\n", " ").strip())
            sys.stdout.flush()
    sys.exit(0)

