#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-14 10:36:36
# Project: cook
#desc:代码里面还没有加入翻页功能  参考：https://blog.csdn.net/qq_36653505/article/details/80573458

from pyspider.libs.base_handler import *
import urllib.parse
import time
import json
import pandas as pd 

class Handler(BaseHandler):
	#配置通用的请求属性
    crawl_config = {
		'headers' : {
		'Connection':'keep-alive',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.8',
      'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	}
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.xiachufang.com/category/', callback=self.index_page)
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('body > div.page-outer > div > div > div > div:nth-child(1) > div.cates-list-all.clearfix > ul> li > a').items():
            print(each)
            self.crawl(each.attr.href,callback=self.list_page)
    @config(age=10*24*60*60)
    def list_page(self,response):
        for each in response.doc('body > div.page-outer > div > div > div.pure-u-2-3.main-panel > div.white-bg.block > div > div.pure-u-3-4.category-recipe-list > div.normal-recipe-list > ul > li > div > div > p.name > a').items():
            print (each)
            self.crawl(each.attr.href,callback=self.detail_page)
	#分页
	for each in response.doc('body > div.page-outer > div > div > div.pure-u-2-3.main-panel > div.white-bg.block > div > div.pure-u-3-4.category-recipe-list > div.pager > a.next').items():
	    self.crawl(each.attr.href,callback=self.list_page)
   
    @config(priority=2)
    def detail_page(self, response):
        zuofa=""
        step=int(1)
        for each in response.doc('li[itemprop="recipeInstructions"]>p[class="text"]'):
            zuofa+=str(step)+":"+each.text+"\n"
            step=step+1
           
            
        print(zuofa)
		return {
			"url": response.url,
			"title": response.doc('.page-title').text(),
			"Material":response.doc('td[class="name"]>a').text(),
			"Consumption":response.doc('.unit').text(),
			"Score":response.doc('span[itemprop="ratingValue"]').text(),
			"step":zuofa,
			"desc":response.doc('.desc.mt30').text()
			}
