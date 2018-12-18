# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request

class MafengwoPipeline(object):
    def process_item(self, item, spider):
        return item
#同步的下载器
class Mafengwo(object):
	def __init__(self):

		self.path = os.path.join(os.path.dirname(__file__),'image')
		if not os.path.exists(self.path):
			os.mkdir(self.path)

	def process_item(self,item,spider):
		
		title = item['title']
		pic_url = item['pic_url']
		
		title_path = os.path.join(self.path,title)
		if not os.path.exists(title_path):
			os.mkdir(title_path)
		for url in pic_url:
			image_name = str(hash(url))
			request.urlretrieve(url,os.path.join(title_path,image_name+'.jpg'))
		

		return item

class Mafengwo2(object):
	def __init__(self):
		self.path = os.path.join(os.path.dirname(__file__),'image')
		if not os.path.exists(self.path):
			os.mkdir(self.path)

	def process_item(self,item,spider):
	
		title = item['title']
		pic_url2 = item['pic_url2']

		title_path = os.path.join(self.path,title)
		
		if not os.path.exists(title_path):
			os.mkdir(title_path)
		for url in pic_url2:
			image_name = str(hash(url))
			request.urlretrieve(url,os.path.join(title_path,image_name+'.jpg'))
		return item
