
from cgitb import text
from enum import EnumMeta
import enum
from importlib.resources import contents
from lib2to3.pgen2.pgen import ParserGenerator
from multiprocessing.context import _default_context
from sqlite3 import paramstyle
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import os
import numpy as np
import pandas as pd
from datetime import datetime
import json
import re



#address_review='/Users/anna/data/review/'
address_review='/Volumes/GoogleDrive/내 드라이브/'
file_name='df_noingi_review'

def review_lowMall(product_id,review_page):
    
    dic_reviews_2 = {
        'buyOption': [],
        'createTime': [],
        
        'mallId': [],
        'mallLogo': [],
        'mallName': [],
        'mallProductId': [],
        'mallReviewId': [],
        'mallSeq': [],
        'matchNvMid': [],
        'modifyDate': [],
        'nvMid': [],
        'pageUrl': [],
        'qualityScore': [],
        'registerDate': [],
        'starScore': [],
        'title': [],
        'topicCount': [],
        'topicYn': [],
        'uniqueKey': [],
        'updateType': [],
        'userId': [],
        
        'list_topics':[],
        
        'content': []

    }

    ############################# review_page 리뷰 페이지 까지 옮기기
    for page in range(1,review_page+1):
        #https://search.shopping.naver.com/catalog/23112786442?query=%EC%9D%98%EC%9E%90&NaPm=ct%3Dl5xm35ds%7Cci%3Da2c1f40865bd2df964f9443587faa435f38b42ca%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3Df56e71721975b26c47f3a0d908e7ccba6c3472d6
        #요청 URL: https://search.shopping.naver.com/api/review?nvMid=23112786442&reviewType=ALL&sort=QUALITY&isNeedAggregation=Y&isApplyFilter=Y&page=1&pageSize=20
        url_review= 'https://search.shopping.naver.com/api/review?nvMid={}&reviewType=ALL&sort=QUALITY&isNeedAggregation=Y&isApplyFilter=Y&page={}&pageSize=20'.format(product_id,page)
        resp=requests.get(url_review)
        time.sleep(5) 
        print('     ',page,'리뷰 페이지 리뷰응답',resp)        
        dic_resp = json.loads(resp.text)
        list_reviews=dic_resp['reviews']
    
        # 현재 리뷰 페이지에서 리뷰 20개 가져오기
        for i,list_review in enumerate(list_reviews):            
            if('buyOption' in list_review.keys()):
                dic_reviews_2['buyOption'].append(list_review['buyOption'])
            else:
                dic_reviews_2['buyOption'].append('')


            dic_reviews_2['content'].append(list_review['content'])
            dic_reviews_2['createTime'].append(list_review['createTime'])
            
            dic_reviews_2['mallId'].append(list_review['mallId'])
            dic_reviews_2['mallLogo'].append(list_review['mallLogo'])
            dic_reviews_2['mallName'].append(list_review['mallName'])
            dic_reviews_2['mallProductId'].append(list_review['mallProductId'])
            dic_reviews_2['mallReviewId'].append(list_review['mallReviewId'])            
            dic_reviews_2['mallSeq'].append(list_review['mallSeq'])
            
            dic_reviews_2['matchNvMid'].append(list_review['matchNvMid'])
            dic_reviews_2['modifyDate'].append(list_review['modifyDate'])
            dic_reviews_2['nvMid'].append(list_review['nvMid'])
            
            if('pageUrl' in list_review.keys()):
                dic_reviews_2['pageUrl'].append(list_review['pageUrl'])
            else:
                dic_reviews_2['pageUrl'].append('')
            
            dic_reviews_2['qualityScore'].append(list_review['qualityScore'])
            dic_reviews_2['registerDate'].append(list_review['registerDate'])
            dic_reviews_2['starScore'].append(list_review['starScore'])
            
            dic_reviews_2['title'].append(list_review['title'])
            dic_reviews_2['topicCount'].append(list_review['topicCount'])
            dic_reviews_2['topicYn'].append(list_review['topicYn'])
            dic_reviews_2['uniqueKey'].append(list_review['uniqueKey'])
            dic_reviews_2['updateType'].append(list_review['updateType'])
            dic_reviews_2['userId'].append(list_review['userId'])
            
            if('topics' in list_review.keys()):
                dic_reviews_2['list_topics'].append(list_review['topics'])
            else:
                dic_reviews_2['list_topics'].append('')
                    
    df_reviews_2=pd.DataFrame(dic_reviews_2)
    df_reviews_2.to_csv(path_or_buf=address_review+file_name+'.csv',encoding = 'utf-8-sig')
    return df_reviews_2
##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################


##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################

df_review=review_lowMall(product_id=17185724140,review_page=22)

##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
