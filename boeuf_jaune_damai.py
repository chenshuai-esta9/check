# -*- coding: utf-8 -*-
import requests
import json
import time
from threading import Timer
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
def check_damai(old_dict):
	#flag=False
	new_spectacles_list=[]
	params = {
		'ctl':	'',
		'cty':	'北京',
		'et':	'2119-12-31',
		'keyword':'砍价',	
		'order': '2',
		'singleChar':''	,
		'st':	'2018-10-10',
		'sctl':'',
		'currPage':'',
		'tsg':	'5'
	}

	url='https://search.damai.cn/searchajax.html'
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Cookie':'cna=JvCmEvRWh0ECAYbWhMtaDB4F; cad=mYP25sOqB8MHUEa5ThwtIDqqQcRJg1We1nzAWaty9IQ=0001; cap=80d7; sca=666cf5b9; atpsida=58b0198555e20c558e98f292_1539087585_2',
		'User-Agent': 'Mozilla/5.0 (X11; Macintosh; Mac OS X 10.9; rv:62.0) Gecko/20100101 Firefox/62.0'
	}
	s=requests.Session()
	s.headers.update(headers)
	r=s.post(url=url, headers=headers, data=params)
	if r.cookies.get_dict():
		s.cookies.update(r.cookies)
	html = r.text
	html = json.loads(html)
	#print(html)
	js = json.dumps(html, sort_keys=True, indent=4, separators=(',', ':'),ensure_ascii=False)
	#print(js)
	inp_dict = json.loads(js)
	#print(type(inp_dict))
	#print (inp_dict)
	#print(len(inp_dict))
	spectacle_list=inp_dict["pageData"]["resultData"]
	spectacle_excited_dict=old_dict
	for spectacle in spectacle_list:
		if spectacle_excited_dict.__contains__(spectacle["projectid"])==False:
			spectacle_excited_dict[spectacle["projectid"]]=spectacle["nameNoHtml"]
			flag=True
			new_spectacles_list.append(spectacle["nameNoHtml"])
	pageNb=inp_dict["pageData"]["totalPage"]
	if pageNb>1:
		for i in range(2,pageNb+1):
			params['currPage']=str(i)
			r=s.post(url=url, headers=headers, data=params)
			if r.cookies.get_dict():
				s.cookies.update(r.cookies)
			html = r.text
			html = json.loads(html)
			js = json.dumps(html, sort_keys=True, indent=4, separators=(',', ':'),ensure_ascii=False)
			inp_dict = json.loads(js)
			spectacle_list=inp_dict["pageData"]["resultData"]
			for spectacle in spectacle_list:
				if spectacle_excited_dict.__contains__(spectacle["projectid"])==False:
					spectacle_excited_dict[spectacle["projectid"]]=spectacle["nameNoHtml"]
					#flag=True
					new_spectacles_list.append(spectacle["nameNoHtml"])
	#print(spectacle_excited_dict.values())
	return spectacle_excited_dict, new_spectacles_list
	#t=t = Timer(300, check_damai)#300s
	#t.start()
old_dict={}
IFTTT_WEBHOOKS_URL="https://maker.ifttt.com/trigger/boeuf_jaune_damai/with/key/nOnDrgqqPgN8Vew9QX_paewfrtap_UGErp3Y-KFBF_c"
while True:
	spectacle_excited_dict, new_spectacles_list=check_damai(old_dict)
	old_dict=spectacle_excited_dict
	#print(old_dict.keys())
	if len(new_spectacles_list)!=0:
		report={}
		report["value1"]=new_spectacles_list
		requests.post(IFTTT_WEBHOOKS_URL, data=report)
		#for new in new_spectacles_list:
			#print(new+'\n')
	time.sleep(300)

#https://maker.ifttt.com/use/nOnDrgqqPgN8Vew9QX_paewfrtap_UGErp3Y-KFBF_c

    