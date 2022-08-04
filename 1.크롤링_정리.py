import requests
from tqdm import tqdm
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
import re


# 네이버 쇼핑 제품 크롤링
# 검색어 : 게이밍 의자
# 페이지 : 1~3
# list_products 만들고 df_products 저장하기!
url = "https://search.shopping.naver.com/api/search/all"
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36}"}

list_products = []
for page_num in range(1, 3):
    params = {
        "sort" : "rel",
        "pagingIndex" : str(page_num) ,
        "pagingSize" : "20",
        "viewType" : "list" ,
        "productSet" : "total",
        "frm" : "NVSHTTL",
        "query" : "게이밍의자",
        "origQuery" : "게이밍의자"
    }

    time.sleep(0.5)

    res = requests.get(url, params=params, headers= headers)
    # print(res.url)
    js = json.loads(res.text)
    prod_infos = js["shoppingResult"]["products"]

    
    for prod_info in prod_infos:
        results = {}
        results["productName"] = prod_info["productName"]
        results["rank"] = prod_info["rank"]
        results["id"] = prod_info["id"]
        results["score"] = prod_info["scoreInfo"]

        results["brand"] = prod_info["brand"]
        results["shop"] = prod_info["mallName"]
        results["maker"] = prod_info["maker"]

        results["price"] = prod_info["price"]
        results["reviewCnt"] = prod_info["reviewCount"]
        results["purchaseCnt"] = prod_info["purchaseCnt"]
        
        
        
        if prod_info["mallProductUrl"] =="":
            # 쇼핑몰 유형 2) lowmalllist 있는 경우 = 서치쇼핑 [id값 필요]
            results["url"] = "https://search.shopping.naver.com/catalog/" + prod_info["id"]
        else :
            # 쇼핑몰 유형 1) lowmalllist 없는 경우 = 스마트쇼핑 [merchantNo,originProductNo값 필요]
            results["url"] = prod_info["mallProductUrl"]
        time.sleep(0.5)

        list_products.append(results)

df_products = pd.DataFrame(list_products)
df_products.to_csv('df_ product.csv',encoding='utf-8-sig')




# list_of_reviews 만들기
# 쇼핑몰 유형 1) lowmalllist 없는 경우 = 스마트쇼핑
# 쇼핑몰 유형 2) lowmalllist 있는 경우 = 서치쇼핑
list_of_reviews = []
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36}"}

for list_product in tqdm(list_products):

    ### 1) 스마트 스토어 리뷰
    if "smartstore" in list_product["url"]:
        review_url = "https://smartstore.naver.com/i/v1/reviews/paged-reviews"

        req = requests.get(list_product["url"], headers = headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        merchantNo = json.loads(soup.select('script')[1].string.split('window.__PRELOADED_STATE__=')[1])['product']['A']['channel']['naverPaySellerNo']
        originProductNo = json.loads(soup.select('script')[1].string.split('window.__PRELOADED_STATE__=')[1])['product']['A']['productNo']



        page_num = 1

        while True:
            params = {
                "page" : page_num,
                "pageSize" : "20",
                "merchantNo" : merchantNo ,
                "originProductNo" : originProductNo ,
                "sortType" : "REVIEW_RANKING"
            }
            time.sleep(0.75)

            res = requests.get(review_url, headers=headers, params=params)
            try:
                reviews = json.loads(res.content)

                for r in reviews["contents"]:
                    review = {}
                    content = re.sub(r"[\t\r\n]|\s{2,}|\x00"," ",r["reviewContent"])
                    score = r["reviewScore"]

                    review["product"] = list_product["productName"]
                    review["rank"] = list_product["rank"]
                    review["brand"] = list_product["brand"]
                    review["maker"] = list_product["maker"]
                    review["shop"] = list_product["shop"]
                    review["userID"]=r["writerMemberId"]
                    review["title"] = ""
                    review["content"] = content
                    review["score"] = score

                    list_of_reviews.append(review)
                
                if reviews["last"]:
                    break
                
                print("="*20, page_num, "="*20)
                page_num += 1
                
            except:
                print(res.text)
                break


####### 2) 서치 네이버 쇼핑 리뷰
    else:

        count = 0
        page_num = 1
        review_url = "https://search.shopping.naver.com/api/review"
        
        while True:

            params = {
                "nvMid" : list_product["id"],
                "reviewType" : "ALL",
                "sort" : "QUALITY" ,
                "isNeedAggregation" : "N",
                "isApplyFilter" : "Y" ,
                "page" : page_num ,
                "pageSize" : "20"
            }

            time.sleep(0.75)
            
            res = requests.get(review_url, headers=headers, params=params)
            try:
                reviews = json.loads(res.content)
                total_count = reviews["totalCount"]

                for r in reviews["reviews"]:
                    review = {}
                    content = re.sub(r"[\t\r\n]|\s{2,}|\x00"," ",r["content"])

                    review["product"] = list_product["productName"]
                    review["rank"] = list_product["rank"]
                    review["brand"] = list_product["brand"]
                    review["maker"] = list_product["maker"]
                    review["shop"] = list_product["shop"]
                    review["userID"]=r["userId"]                    
                    review["title"] = re.sub(r"\x00"," ",r["title"])
                    review["content"] = content
                    review["score"] = r["starScore"]

                    list_of_reviews.append(review)

                    count += 1
                
                if total_count == count:
                    break
                
                print("="*20, page_num, "="*20)

                page_num += 1
                
            except:
                print(res.text)
                break

df_list_of_reviews = pd.DataFrame(list_of_reviews)
df_list_of_reviews.to_csv("product_review.csv", encoding='utf-8-sig')

