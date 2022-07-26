from enum import EnumMeta
import enum
from importlib.resources import contents
from sqlite3 import paramstyle
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import re
from logging.config import DEFAULT_LOGGING_CONFIG_PORT
from operator import index




address_product='/Users/anna/data/product/'
address_review='/Users/anna/data/review/'
'''
address_product='C:/data/product/'
address_review='C:/data/review/'
'''

max_reviewPage=90
sleep_time=6

# 최대 100page = 20*100 =2000개의 리뷰
# 현재 5페이지만 가져옴. 40*5 = 200개의 제품
lastPage=5

dic_products = {
    'price':[],
    'openDate':[],
    'purchaseCnt':[],
    'rank' : [],
    'reviewCount':[],
    'reviewCountSum':[],
    'shopNNo':[],

    'crUrl':[],
    'crUrlMore' : [],
    
    'productName' : [],
    'productTitle' : [],
    'productTitleOrg':[],
    
    'brand' : [],
    'brandNo':[],
    'maker' : [],
    'makerNo':[],
    'mallPcUrl':[],
    'list_mallInfoCache':[],

    'deliveryFeeContent':[],
    'lowPrice':[],
    'scoreInfo':[],

    # 1) lowmall_none = merchanNO,OriginProductNo
    'lowMallList':[],
    'chnlSeq':[],
    'mallProductId':[],
    # 2) lowmall = id => NvMid
    'id':[],
    #3) 리빙윈도 웹페이지 일때 REVIEW 가져오기
    'wdNm':[],
    
    
    'characterValue':[]
    }

# 1페이지부터 lastPage까지 페이지 넘기기
for product_page in range(1,lastPage+1):
    #https://search.shopping.naver.com/api/search/all?sort=rel&pagingIndex=1&pagingSize=40&viewType=list&productSet=total&deliveryFee=&deliveryTypeValue=&frm=NVSHTTL&query=%EC%9D%98%EC%9E%90&origQuery=%EC%9D%98%EC%9E%90&iq=&eq=&xq=&spec=M10007003%7CM10758117&window='
    request_url_page='https://search.shopping.naver.com/api/search/all?sort=rel&pagingIndex={}&pagingSize=40&viewType=list&productSet=total&deliveryFee=&deliveryTypeValue=&frm=NVSHTTL&query=%EC%9D%98%EC%9E%90&origQuery=%EC%9D%98%EC%9E%90&iq=&eq=&xq=&spec=M10007003%7CM10758117&window='.format(product_page)
    print(request_url_page)
    resp = requests.get(request_url_page)
    time.sleep(sleep_time) #네이버에서 봇으로 인식하므로 3초간의 딜레이를 넣음.
    print(product_page,'번째 page 서버응답',resp)
    dic_resp = json.loads(resp.text)
    ############################## 해당 페이지 제품 리스트
    dic_shoppingResult=dic_resp['shoppingResult']
    list_products = dic_resp['shoppingResult']['products']

        ## 0~39 번째 상품 ->dic_products
    for i,list_product in enumerate(list_products):
        
        dic_products['id'].append(list_product['id'])
        dic_products['price'].append(list_product['price'])
        dic_products['openDate'].append(list_product['openDate'])
        dic_products['purchaseCnt'].append(list_product['purchaseCnt'])
        dic_products['rank'].append(list_product['rank'])
        dic_products['reviewCount'].append(list_product['reviewCount'])
        dic_products['reviewCountSum'].append(list_product['reviewCountSum'])
        dic_products['shopNNo'].append(list_product['shopNNo'])


        dic_products['crUrl'].append(list_product['crUrl'])
        dic_products['crUrlMore'].append(list_product['crUrlMore'])
        
        dic_products['productName'].append(list_product['productName'])
        dic_products['productTitle'].append(list_product['productTitle'])
        print(i ,list_product['productTitle'])
        dic_products['productTitleOrg'].append(list_product['productTitleOrg'])

        
    
        dic_products['brand'].append(list_product['brand'])
        dic_products['brandNo'].append(list_product['brandNo'])
        dic_products['maker'].append(list_product['maker'])
        dic_products['makerNo'].append(list_product['makerNo'])
        dic_products['mallPcUrl'].append(list_product['mallPcUrl'])
        
        if('mallInfoCache' in list_product.keys()):
            dic_products['list_mallInfoCache'].append(list_product['mallInfoCache'])
        else:
            dic_products['list_mallInfoCache'].append('')

    
    
        dic_products['deliveryFeeContent'].append(list_product['deliveryFeeContent'])
    
        dic_products['characterValue'].append(list_product['characterValue'])
        dic_products['lowMallList'].append(list_product['lowMallList'])
        dic_products['lowPrice'].append(list_product['lowPrice'])
        
        dic_products['chnlSeq'].append(list_product['chnlSeq'])
        dic_products['mallProductId'].append(list_product['mallProductId'])
        dic_products['wdNm'].append(list_product['wdNm'])
        
        dic_products['scoreInfo'].append(list_product['scoreInfo'])


df_products=pd.DataFrame(dic_products)
df_products.to_csv(path_or_buf=address_product+'df_products_{}페이지까지.csv'.format(lastPage),encoding = 'utf-8-sig')




##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################


#페이로드 실패 상품
dic_fail_product={}

##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
# 1) lowmall_none = merchanNO,OriginProductNo
# 1) lowMall 이 없는 웹페이지 일때 REVIW 가져오기
def review_lowMall_none(product_index,merchantNo,originProductNo,reviewCount):
    dic_reviews_1 = {
        'channelId':[],
        'channelServiceType':[],
        'createDate':[],
    
        'detailCategorizeCategoryId':[],
    
        'freeTrialReview':[],
    
        'id':[],
        'isMyReview':[],
        'largeCategorizeCategoryId':[],
        'middleCategorizeCategoryId':[],

    
        'originProductNo':[],
        'productName':[],
        'productNo':[],
        'productOptionContent':[],
        'productUrl':[],
        'profileImageSourceType':[],
    
        'list_reviewAttaches':[],
    
        'reviewContentClassType':[],
        'reviewDisplayStatusType':[],
        'reviewEvaluationValueSeqs':[],
        'reviewRankingScore':[],
        'reviewScore':[],
        'reviewServiceType':[],
    
        'reviewType':[],

    
        'list_reviewTopics':[],
    
        'writerMemberId':[],
        'writerMemberMaskedId':[],
        'writerMemberNo':[],
        'writerMemberProfileImageUrl':[],
        
        'reviewContent':[]
    }

    review_page=reviewCount//20+1
    if(review_page>max_reviewPage): review_page=max_reviewPage+1
    
    ############################# review_page 리뷰 페이지 까지 옮기기
    for page in range(1,review_page+1):
        #merchantNo=500007644
        #originProductNo=109072854
        #https://smartstore.naver.com/i/v1/reviews/paged-reviews?page=1&pageSize=20&merchantNo=500169113&originProductNo=6299178421&sortType=REVIEW_RANKING
        url_review= 'https://smartstore.naver.com/i/v1/reviews/paged-reviews?page={}&pageSize=20&merchantNo={}&originProductNo={}&sortType=REVIEW_RANKING'.format(page,merchantNo,originProductNo)
        resp=requests.get(url_review)
        time.sleep(sleep_time) 
        print('     ',page,'리뷰 페이지 리뷰응답',resp)

        if resp.text=='OK':
            print('     originProductNo,merchantNo 다름=실패')
            print('     실패 1번유형 product:',product_index , merchantNo, originProductNo)
            dic_fail_product[product_index]=[1,merchantNo,originProductNo]
            return 
        
        dic_resp = json.loads(resp.text)
        list_contents=dic_resp['contents']
        # 현재 리뷰 페이지에서 리뷰 20개 가져오기
        for i,list_content in enumerate(list_contents):
            #print(i,'번째 리뷰')
            dic_reviews_1['channelId'].append(list_content['channelId'])
            dic_reviews_1['channelServiceType'].append(list_content['channelServiceType'])
            dic_reviews_1['createDate'].append(list_content['createDate'])

            if('detailCategorizeCategoryId' in list_content.keys()):
                dic_reviews_1['detailCategorizeCategoryId'].append(list_content['detailCategorizeCategoryId'])
            else:
                dic_reviews_1['detailCategorizeCategoryId'].append('')
    
            if('freeTrialReview' in list_content.keys()):
                dic_reviews_1['freeTrialReview'].append(list_content['freeTrialReview'])
            else:
                dic_reviews_1['freeTrialReview'].append('')



            dic_reviews_1['id'].append(list_content['id'])
            dic_reviews_1['isMyReview'].append(list_content['isMyReview'])
            dic_reviews_1['largeCategorizeCategoryId'].append(list_content['largeCategorizeCategoryId'])
            dic_reviews_1['middleCategorizeCategoryId'].append(list_content['middleCategorizeCategoryId'])
    
    
    
            dic_reviews_1['originProductNo'].append(list_content['originProductNo'])
            dic_reviews_1['productName'].append(list_content['productName'])
            dic_reviews_1['productNo'].append(list_content['productNo'])

            if('productOptionContent' in list_content.keys()):
                dic_reviews_1['productOptionContent'].append(list_content['productOptionContent'])
            else:
                dic_reviews_1['productOptionContent'].append('')
                
            dic_reviews_1['productUrl'].append(list_content['productUrl'])
            dic_reviews_1['profileImageSourceType'].append(list_content['profileImageSourceType'])                                            



            dic_reviews_1['list_reviewAttaches'].append(list_content['reviewAttaches'])    
    
    
            dic_reviews_1['reviewContentClassType'].append(list_content['reviewContentClassType'])
            dic_reviews_1['reviewDisplayStatusType'].append(list_content['reviewDisplayStatusType'])
            if('reviewEvaluationValueSeqs' in list_content.keys()):
                dic_reviews_1['reviewEvaluationValueSeqs'].append(list_content['reviewEvaluationValueSeqs'])
            else:
                dic_reviews_1['reviewEvaluationValueSeqs'].append('')

            
            dic_reviews_1['reviewRankingScore'].append(list_content['reviewRankingScore'])
            dic_reviews_1['reviewScore'].append(list_content['reviewScore'])
            dic_reviews_1['reviewServiceType'].append(list_content['reviewServiceType'])


            dic_reviews_1['reviewType'].append(list_content['reviewType'])                                            
            dic_reviews_1['reviewContent'].append(list_content['reviewContent'])                                            

            if('reviewTopics' in list_content.keys()):
                dic_reviews_1['list_reviewTopics'].append(list_content['reviewTopics'])
            else:
                dic_reviews_1['list_reviewTopics'].append('')


            dic_reviews_1['writerMemberId'].append(list_content['writerMemberId'])
            dic_reviews_1['writerMemberMaskedId'].append(list_content['writerMemberMaskedId'])
            dic_reviews_1['writerMemberNo'].append(list_content['writerMemberNo'])
            dic_reviews_1['writerMemberProfileImageUrl'].append(list_content['writerMemberProfileImageUrl'])
    
    
    ############################# review_page 페이지까지 리뷰 페이지 정보 다 저장함.        
    df_reviews_1=pd.DataFrame(dic_reviews_1)
    df_reviews_1.to_csv(path_or_buf=address_review+'{}_df_reviews1_{}페이지까지.csv'.format(product_index,review_page),encoding = 'utf-8-sig')
#############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
# 2) lowMall 이 았는 웹페이지 일때 REVIW 가져오기
# 2) lowmall = id => NvMid
def review_lowMall(product_index,product_id,reviewCount):
    
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
    
    review_page=reviewCount//20+1
    if(review_page>max_reviewPage): review_page=max_reviewPage+1

    ############################# review_page 리뷰 페이지 까지 옮기기
    for page in range(1,review_page+1):
        #https://search.shopping.naver.com/catalog/23112786442?query=%EC%9D%98%EC%9E%90&NaPm=ct%3Dl5xm35ds%7Cci%3Da2c1f40865bd2df964f9443587faa435f38b42ca%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3Df56e71721975b26c47f3a0d908e7ccba6c3472d6
        #요청 URL: https://search.shopping.naver.com/api/review?nvMid=23112786442&reviewType=ALL&sort=QUALITY&isNeedAggregation=Y&isApplyFilter=Y&page=1&pageSize=20
        url_review= 'https://search.shopping.naver.com/api/review?nvMid={}&reviewType=ALL&sort=QUALITY&isNeedAggregation=Y&isApplyFilter=Y&page={}&pageSize=20'.format(product_id,page)
        resp=requests.get(url_review)
        time.sleep(sleep_time) 
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
                

                
    ############################# 1~2 페이지까지 리뷰 페이지 정보 다 저장함.        
    df_reviews_2=pd.DataFrame(dic_reviews_2)
    df_reviews_2.to_csv(path_or_buf=address_review+'{}_df_reviews2_{}페이지까지.csv'.format(product_index,review_page),encoding = 'utf-8-sig')
##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#3) 리빙윈도 웹페이지 일때 REVIEW 가져오기
def review_livingWindow(product_index,merchantNo,originProductNo):

    dic_reviews_3 = {
        'channelId':[],
        'channelServiceType':[],
        'createDate':[],
    
        'detailCategorizeCategoryId':[],
    
        'freeTrialReview':[],
    
        'id':[],
        'isMyReview':[],
        'largeCategorizeCategoryId':[],
        'middleCategorizeCategoryId':[],

    
        'originProductNo':[],
        'productName':[],
        'productNo':[],
        'productOptionContent':[],
        'productUrl':[],
        'profileImageSourceType':[],
    
        'list_reviewAttaches':[],
    
        'reviewContentClassType':[],
        'reviewDisplayStatusType':[],
        'reviewEvaluationValueSeqs':[],
        'reviewRankingScore':[],
        'reviewScore':[],
        'reviewServiceType':[],
    
        'reviewType':[],
            
        'list_reviewTopics':[],
    
        'writerMemberId':[],
        'writerMemberMaskedId':[],
        'writerMemberNo':[],
        'writerMemberProfileImageUrl':[],
        
        'reviewContent':[]

    }
    
    review_page=reviewCount//20+1
    if(review_page>max_reviewPage): review_page=max_reviewPage+1

    ############################# review_page 리뷰 페이지 까지 옮기기
    for page in range(1,review_page+1):
        #'https://shopping.naver.com/v1/reviews/paged-reviews?_nc_=1658502000000&page=1&pageSize=20&merchantNo='100965934'&&sortType=REVIEW_RANKING'
        #요청 URL: https://shopping.naver.com/v1/reviews/paged-reviews?_nc_=1658502000000&page=1&pageSize=20&merchantNo=500039008&originProductNo=4487772364&sortType=REVIEW_RANKING

        url_review= 'https://shopping.naver.com/v1/reviews/paged-reviews?_nc_=1658502000000&page={}&pageSize=20&merchantNo={}&originProductNo={}&sortType=REVIEW_RANKING'.format(page,merchantNo,originProductNo)

        resp=requests.get(url_review)
        time.sleep(sleep_time) #네이버에서 봇으로 인식하므로 1초간의 딜레이를 넣음.
        print('     ',page,'리뷰 페이지 리뷰응답',resp)
        if resp.text=='OK':
            print('     originProductNo,merchantNo 다름=실패')
            print('     실패 3번유형 product:',product_index , merchantNo, originProductNo)
            dic_fail_product[product_index]=[3,merchantNo,originProductNo]
            return 

        dic_resp = json.loads(resp.text)
        list_contents=dic_resp['contents']
    
        # 현재 리뷰 페이지에서 리뷰 20개 가져오기
        for i,list_content in enumerate(list_contents):
            dic_reviews_3['channelId'].append(list_content['channelId'])
            dic_reviews_3['channelServiceType'].append(list_content['channelServiceType'])
            dic_reviews_3['createDate'].append(list_content['createDate'])

            dic_reviews_3['detailCategorizeCategoryId'].append(list_content['detailCategorizeCategoryId'])
    
    
            if('freeTrialReview' in list_content.keys()):
                dic_reviews_3['freeTrialReview'].append(list_content['freeTrialReview'])
            else:
                dic_reviews_3['freeTrialReview'].append('')



            dic_reviews_3['id'].append(list_content['id'])
            dic_reviews_3['isMyReview'].append(list_content['isMyReview'])
            dic_reviews_3['largeCategorizeCategoryId'].append(list_content['largeCategorizeCategoryId'])
            dic_reviews_3['middleCategorizeCategoryId'].append(list_content['middleCategorizeCategoryId'])
    
    
    
            dic_reviews_3['originProductNo'].append(list_content['originProductNo'])
            dic_reviews_3['productName'].append(list_content['productName'])
            dic_reviews_3['productNo'].append(list_content['productNo'])

            if('productOptionContent' in list_content.keys()):
                dic_reviews_3['productOptionContent'].append(list_content['productOptionContent'])
            else:
                dic_reviews_3['productOptionContent'].append('')
                
            dic_reviews_3['productUrl'].append(list_content['productUrl'])
            dic_reviews_3['profileImageSourceType'].append(list_content['profileImageSourceType'])                                            



            dic_reviews_3['list_reviewAttaches'].append(list_content['reviewAttaches'])    
    
    
            dic_reviews_3['reviewContentClassType'].append(list_content['reviewContentClassType'])
            dic_reviews_3['reviewDisplayStatusType'].append(list_content['reviewDisplayStatusType'])
            dic_reviews_3['reviewEvaluationValueSeqs'].append(list_content['reviewEvaluationValueSeqs'])
            dic_reviews_3['reviewRankingScore'].append(list_content['reviewRankingScore'])
            dic_reviews_3['reviewScore'].append(list_content['reviewScore'])
            dic_reviews_3['reviewServiceType'].append(list_content['reviewServiceType'])


            dic_reviews_3['reviewType'].append(list_content['reviewType'])                                            
            dic_reviews_3['reviewContent'].append(list_content['reviewContent'])                                            

            if('reviewTopics' in list_content.keys()):
                dic_reviews_3['list_reviewTopics'].append(list_content['reviewTopics'])
            else:
                dic_reviews_3['list_reviewTopics'].append('')


            dic_reviews_3['writerMemberId'].append(list_content['writerMemberId'])
            dic_reviews_3['writerMemberMaskedId'].append(list_content['writerMemberMaskedId'])
            dic_reviews_3['writerMemberNo'].append(list_content['writerMemberNo'])
            dic_reviews_3['writerMemberProfileImageUrl'].append(list_content['writerMemberProfileImageUrl'])
            
    df_reviews_3=pd.DataFrame(dic_reviews_3)
    df_reviews_3.to_csv(path_or_buf=address_review+'{}_df_reviews3_{}페이지까지.csv'.format(product_index,review_page),encoding = 'utf-8-sig')
##########################################################################################################################################################




#0~39 for 문 -> 0번째 상품~ 39번째 상품 리뷰 데이터 저장하기 review_0.csv
#페이지 구분 리뷰 가져오기 1.LOWMALL_NONE 2. LOWMMALL 3. LIVINGWINDOW##################################################################################################################################################################   
for i in range(len(dic_products['id'])):
    product_index=i
    reviewCount=dic_products['reviewCount'][i]

    merchantNo=dic_products['chnlSeq'][i]
    originProductNo=dic_products['mallProductId'][i]
    product_id=dic_products['id'][i]
    
    
    # 3) 리빙윈도 
    if dic_products['wdNm'][i] ==  '리빙윈도':
        print(i,'번째 상품 -> 3)리빙윈도 : ',dic_products['wdNm'][i])
        review_livingWindow(product_index,merchantNo,originProductNo)
        continue

    
    # 1) lowmall_none = merchanNO,OriginProductNo
    if dic_products['lowMallList'][i] is None:
        print(i,'번째 상품 -> 1) lowMall_none')
        review_lowMall_none(product_index,merchantNo,originProductNo,reviewCount)
        
    # 2) lowmall = id => NvMid
    else:
        print(i,'번째 상품 -> 2) lowMall')
        review_lowMall(product_index,product_id,reviewCount)


#페이로드 실패 상품
df_fail_product=pd.DataFrame(dic_fail_product)
df_fail_product.to_csv(path_or_buf=address_product+'df_fail_product.csv',encoding = 'utf-8-sig')
