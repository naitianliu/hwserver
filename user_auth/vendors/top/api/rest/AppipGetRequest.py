'''
Created by auto_sdk on 2014.11.26
'''
from user_auth.vendors.top.api.base import RestApi
class AppipGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'taobao.appip.get'
