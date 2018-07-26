#!/usr/bin/env python
#encoding:utf8
import BaseHTTPServer
import urllib
import urlparse
import json
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from spider_page import PageSpider

default_request_headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Cache-Control": "max-age=0",
        "cookie": 'abtest=20171109111113261_40; mba_muid=1508128976776538689345; subAbTest=20180207143346600_16; __utma=122270672.1824802916.1518432858.1518432858.1518432858.1; __utmz=122270672.1518432858.1.1.utmcsr=jd.com|utmccn=(referral)|utmcmd=referral|utmcct=/brand.aspx; mhome=1; intlIpLbsCountrySite=jd; ipLocation=%u5317%u4EAC; cn=0; visitkey=22085234461246304; shshshfpa=ac6055d1-5a0f-faf2-d83d-870346fa19c9-1525782489; _jrda=3; pinId=Rfh6dm3BQZg9zHOO2ZAcQu5deekaslCb; cid=9; webp=1; shshshfpb=0049f682412424aab130ca191908349c5b321f0c77a4eb0625afa553b3; TrackID=1KB3e1xjQgsoz-mMtchaHAF7aNNsZEHHet4Y_Tct82mbQl-jhb0aSSL1UEb9XKUzxnw4CoeiytXfZgHqCtv4aejV9TZMpWabEz1-6m7JGtB8; user-key=b54808d6-c09a-43bf-8657-e96d3dc71b4c; areaId=1; ipLoc-djd=1-72-4137-0; 3AB9D23F7A4B3C9B=6AOWWBOZY4D4K5VTDMSZ6IY34TYXURCTGR233YZGFERCF6KWGQ3RONVFBWIKZK7BT2TNSNA4G7DYYWVRI6OCUH4PXA; M_Identification=908350cdfd7d9861_b5fc72e3141ca1985df5b5ef7412c5cd; M_Identification_abtest=20180613193718168_31178555; sc_width=1920; __jdc=122270672; mobilev=html5; PCSYCityID=1; m_uuid_new=E31233748E677283335169AAF9EE2D3E; wxa_level=1; M_Identification=908350cdfd7d9861_b5fc72e3141ca1985df5b5ef7412c5cd; unpl=V2_ZzNtbRYDRkB9CU9SfBFUVWIARV1LAhETd1hPXXNNWwxmVBQNclRCFXwUR1NnGlsUZwMZWEJcQhZFCHZXfBpaAmEBFl5yBBNNIEwZDjl3VQJiBxRUS1JHEnU4dld7KVwEVwMWXEtXQBx9DkFSfR5YB24EG1VAUkclRQ92ZEsbWARmAhZtQ2dCJTdcGlF8H1oHYk4SWUNeQxZ8AEBTfR9bAWUKFVRKVUYRRQl2Vw%3d%3d; CCC_SE=ADC_qFqdnx1SLSoMDBklqbhZkkToT6o1uVcRn87b1Eu8p5%2bpHL%2fOaoYqNrcMMmlmGHPQTplJIvt6EkMzVd3s73NsF%2bHm%2fuJio1w3DdmDMW1CnYSUJoEl58RyUf%2fRuBk8O1izDVHrrSIwLd92nnCUuCrAtTc5ySLuL3YvW5dGjzOP%2biyZuf3E29x1gVSR%2fvbljF0uxQ0WWxt7AVDfxfCp67raCtmOB5zsnSymety4kgavIzi2Cl9GuKM%2bgnUS14DFL9PXrrgVxXP7NtsDuXEj4%2byDKEP80o7j3E%2bM6fSjpcN2Z7XL1S7%2bApOVfiFx0JDVPvhbWix8d31h97Dv5WdyoqtBs8FzRsaymDbZ2tEE1mU3pCH0518kNptDl4k%2f%2bWQgPh%2fYlNUlsCpZLtuwhOtEvI%2flQZFZGgCRfTjoUs6ENV6wDjuhhaELMT2VqDOQj94Zm58yPEUG1FBD73HzWsfDhyemJ%2bcMbZyWD3kJpb8x0nwUz0UshSUflmHTQgjEvdVdBNsG70%2fVy2wgd8%2byhwT5%2ftVy0tgPliSx2hCQgGva%2bvQLIOY7jUeg3l1ruumk3BsVhTVTGmx4fy3h5AV%2bW8TOAc%2bS%2f1D8gZvb%2fFQfcWFB2tsqxxaTqPl662nHlJ6rcLNx6NTHsZ9293cDY2va1wD8mye15a4OC%2ffexaYblqKZUT60oKfdyTcPaHT7Udb0N75fbGuvZSMCh%2bsTvkUdbBujVkftLu5KMzXBZEVMFHhRPne9%2fWM%3d; autoOpenApp_downCloseDate_auto=1529984464080_21600000; sid=e95881b4d696475e419578ccdc2d3c6c; USER_FLAG_CHECK=15ec146a35c38be37fde66c113909b2e; wq_area=1_0_0%7C3; retina=1; warehistory="16580586466,6083201,1431758,11056704,29075555026,11794447957,21860483948,16580068432,5798250,5131291,6748052,6784494,620488,28071169845,23185960933,28069983340,27629434242,26359347852,13374108978,11605492,10290142,11600934,2689458,11439252922,214591,22562886791,26512709810,12551276540,5646656,1964546,25446038164,25446038168,1297263,1104843379,12738538698,26462916859,5295386,4481541,10938418734,3133921,5965059,6389983,3133823,4483110,319438,1220743,6053552,6375090,5284275,5706775,5924244,6051045,6051678,5924270,5168733,5180905,27285455014,10260770177,"; wq_logid=1529992973.71282484; PPRD_P=UUID.1508128976776538689345-LOGID.1529992975426.125596736-CT.137886.1.63; intlIpLbsCountryIp=220.181.38.110; __jdu=1508128976776538689345; mt_xid=V2_52007VwMWU1RYUVMXTx5aA2AHEFtaUVpYGk0pDwdgAxdaVFpOW0saTEAAMlBCTg1QVF8DThEPA24BG1RYCFcNL0oYXAx7AhVOXl9DWhpCGF4OZwciUG1YYlkcSBtbB2IAE2JdXVRd; __jda=122270672.1508128976776538689345.1508128977.1529992364.1529993360.180; __jdv=122270672|baidu|-|organic|not set|1529993360092; shshshfp=f20f0d9c8f441da1431d536cd650d6a4; __jdb=122270672.4.1508128976776538689345|180.1529993360; mba_sid=15299927057535947038975527303.11; __wga=1529994548073.1529992706278.1529924305443.1526355258941.8.28; shshshsID=0854e73b5fe596a758bc293c3f317a3c_23_1529994548522'}


class HttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _process_jd_search(self, keyword):
        if keyword == None:
            return
        url_temp = "http://wqsou.jd.com/search/searchn?key=<keyword>"
        #url_temp = "http://so.m.jd.com/ware/search.action?keyword=<keyword>"
        url = url_temp.replace("<keyword>", urllib.quote_plus(keyword))
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1")
        driver = webdriver.PhantomJS()
        driver.get(url)
        self.wfile.write(driver.page_source.encode("utf8", "ignore"))

    def _process_jd_search_json(self, keyword):
        url_temp = 'https://so.m.jd.com/ware/search._m2wq_list?keyword=<query>&datatype=1&callback=jdSearchResultBkCbA&page=1&pagesize=10&ext_attr=no&brand_col=no&price_col=no&color_col=no&size_col=no&ext_attr_sort=no&merge_sku=yes&multi_suppliers=yes&area_ids=1,72,2819&qp_disable=no&fdesc=%E5%8C%97%E4%BA%AC&t1=<time>'
        ps = PageSpider(headers = default_request_headers)
        url = url_temp.replace("<query>", urllib.quote_plus(keyword)).replace("<time>", str(int(time.time())))
        ret = ps.crawl_page(url)
        self.wfile.write(self._format_jd_search_html(ret))
    def _format_jd_search_html(self, json_str):
        json_str = json_str[20:-2].replace("\\x", "\\u00")
        j = json.loads(json_str, "utf8")
        j = j.get("data", {}).get("searchm", {}).get("Paragraph", {})
        html = '<html>'
        html += '<meta http-equiv=Content-Type content="text/html;charset=utf-8">'
        html += '<body><pre>'
        html += "<table>"
        idx = 1
        for i in j:
            fid = i.get("cid1", "").encode("utf8")
            sid = i.get("cid2", "").encode("utf8")
            tid = i.get("catid", "").encode("utf8")
            cat = "%s,%s,%s" % (fid, sid, tid)
            warename = i.get("Content", {}).get("warename", "").encode("utf8")
            imageurl = i.get("Content", {}).get("imageurl", "").encode("utf8")
            imageurl = "//img10.360buyimg.com/n2/s240x240_%s!q70.jpg.webp" % imageurl
            commentcount = i.get("commentcount", "").encode("utf8")
            dredisprice = i.get("dredisprice", "0").encode("utf8")
            good = i.get("good", "0").encode("utf8")
            wareid = i.get("wareid", "0").encode("utf8")
            shop_id = i.get("shop_id", "0").encode("utf8")
            url = "https://item.m.jd.com/product/%s.html" % wareid
            html += "<tr><td><b>" + str(idx) + ". &nbsp;<a href='" + url + "' target=_blank>" + warename + "</a>&nbsp;</b>"
            html += "<tr><td><img src='" + imageurl + "' height='100' weight='100'></td></tr>"
            html += "<tr><td style='color:black'>【价格】%s</td></tr>" % (dredisprice)
            html += "<tr><td style='color:black'>【分类】<a href='https://list.jd.com/list.html?cat=%s'>%s</a></td></tr>" % (cat, cat)
            html += "<tr><td style='color:black'>【shop】<a href='https://shop.m.jd.com/?shopId=%s'>%s</a></td></tr>" % (shop_id, shop_id)
            html += "<tr><td style='color:black'>【评论】%s&nbsp;%s%%</td></tr>" % (commentcount, good)
            
            idx += 1
            html += "</td></tr>"

        html += "</table>"
        html += '</pre></body></html>'
        return html



    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        path = self.path  
        query = urllib.splitquery(path)
        params = dict([(k, v[0]) for k, v in urlparse.parse_qs(query[1]).items()])
        action = params.get("action")
        if action == "jd_search":
            self._process_jd_search_json(params.get("keyword", None))
