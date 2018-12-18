# -*- coding: utf-8 -*-
# 下载图片部分是同步的，有待加强。缺随机ip，ua头，数据库
import scrapy
from mafengwo.items import MafengwoItem 
import json,re

class MaSpider(scrapy.Spider):
    name = 'ma'
    host = 'http://www.mafengwo.cn'
    start_urls = ['http://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi?&params=%7B%22type%22%3A0%2C%22objid%22%3A0%2C%22page%22%3A2%2C%22ajax%22%3A1%2C%22retina%22%3A1%7D&_=1544975097468']

    #从首页获取每一页的入口
    def parse(self, response):
    	a = json.loads(response.text)
    	a = str(a)
    	a = re.findall(r'<a href="(/i/.*?.html)"',a)
    	a = set(a)
    	for i in a:
    		i = self.host + i
    		yield scrapy.Request(url = i,callback = self.run)
    	for n in range(1,45):
    		next = 'http://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi?&params={"type":0,"objid":0,"page":%s,"ajax":1,"retina":1}'%n
    		yield scrapy.Request(url = next,callback = self.parse)

    #访问文章及收集seq值
    def run(self,response):
    	item = MafengwoItem()

    	url = response.url
    	new_url = url.split('/')[-1]
    	idnum = new_url.replace('.html','')#每一篇文章的id参数的值

    	title = response.xpath('//*[@id="_j_cover_box"]/div[3]/div[2]/div/h1/text()').extract()
    	print(title)
    	
    	if title == []:
    		title = response.xpath('//*[@id="_j_cover_box"]/div[5]/div[2]/div/h1/text()').extract()
    	title = str(title)
    	self.title = title.replace("['",'').replace("']",'')
    	
    	item['title'] = self.title
    	item['pic_url'] = re.findall(r'data-rt-src="(.*?)"',response.text)#第一分页所有的图片链接在一个列表里
    	yield item
	    
    	seq_last = re.findall(r'data-seq="(.*?)"',response.text)
    	if seq_last != []:
    		seq_last = seq_last[-1]
	    	detail_url = 'http://www.mafengwo.cn/note/ajax.php?act=getNoteDetailContentChunk&id=%s&seq=%s'%(idnum,seq_last)
	    	yield scrapy.Request(url = detail_url,callback = self.long)

	#访问文章的分页	
    def long(self,response):
    	item = MafengwoItem()
    	idnum = response.url
    	idnum = idnum.split('&')[-2]
    	idnum = idnum.replace('id=','')#为了id值

    	text = json.loads(response.text)
    	text = str(text)
    	
     	pic_url2 = re.findall(r'data-rt-src="(.*?)"',text)#剩余分页的图片url
     	item['pic_url'] = pic_url2
     	if pic_url2 != []:
     		item['pic_url'] = pic_url2
     		item['title'] = self.title
     		yield item

     		seq_last = re.findall(r'data-seq="(.*?)"',text)#最后一个seq值
     		if seq_last != []:
	     		seq_last = seq_last[-1]
	     		detail_url = 'http://www.mafengwo.cn/note/ajax.php?act=getNoteDetailContentChunk&id=%s&seq=%s'%(idnum,seq_last)
	     		yield scrapy.Request(url = detail_url,callback = self.long)
