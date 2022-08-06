
from cgitb import text
from enum import EnumMeta
import enum
from importlib.resources import contents
from lib2to3.pgen2.pgen import ParserGenerator
from multiprocessing.context import _default_context
from sqlite3 import paramstyle
import string
from regex import W
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
from konlpy.tag import Okt # komoran, hannanum, kkma, mecab
import os
import numpy as np
import pandas as pd
from datetime import datetime
import json
import re
from tqdm import tqdm




address_review='/Volumes/GoogleDrive/내 드라이브/'
##address_review='C:/data/review/'
file_name='kss_noingi_review'




def preprocessing(review):
    okt = Okt()
    f = open(address_review+'stopwords_noingi.txt', encoding="utf-8")
    stop_words = f.read().split()
    
    g = open(address_review+'noingi_good_dic.txt', encoding="utf-8")
    noingi_good_dic = g.read().split()
    
    # 1. 한글 및 공백을 제외한 문자 모두 제거.
    review_text = re.sub("[^가-힣\\s]", "", review)
    # sub -> replace
    # 2. okt 객체를 활용해서 형태소 토큰화 + 품사 태깅(pos)
    # stem = 어간추출 -> 통일화
    word_review = okt.pos(review_text, stem=True)
    
    # 사전 단어 나올시 문장 자체를 삭제
    for (token,pos) in word_review:
        if token in noingi_good_dic:
            return ['']
    # 노이즈 & 불용어 제거
    # _ 품사 자리 , pos 라고 잡아도 됨
    # _ : place holder. = 자리 지킴이
    word_review = [(token,pos) for token, pos in word_review if not token in stop_words and not token in noingi_good_dic and len(token) > 1]
    
    # 명사, 동사, 형용사 추출
    word_review = [token for token, pos in word_review if pos in ['Noun','Adjective']]
    return word_review



def df_word_bad(list1_bad):
    df_word_bad = pd.DataFrame(list1_bad,columns=['word'])
    df_word_bad.to_csv(path_or_buf=address_review+file_name+'_bad_bigram'+'.csv',encoding = "cp949")
    return df_word_bad


def df_valuecounts_bad(df_word_bad):
    df_valuecounts_bad=df_word_bad['word'].value_counts()
    df_valuecounts_bad.to_csv(path_or_buf=address_review+file_name+'_bad_valuecount_bigram'+'.csv',encoding = "cp949")


#return [' '.join(list_tokens[i:i+2]) for 5i in range(len(list_tokens)-1)]
def my_tokenizer_with_bigram(list_tokens):
    list_d=[]
    for i in range(len(list_tokens)-1):
        if(list_tokens[i]=='' or list_tokens[i+1]==''):
            continue
        list_d.append(' '.join(list_tokens[i:i+2]))
    return list_d
        


##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################

df_noingi = pd.read_csv(address_review+file_name+'.csv', header=0)
df_noingi.drop(df_noingi.columns[0],axis=1,inplace=True)


list_bad=[]
for index in tqdm(range(len(df_noingi))):
    for i,v in enumerate(df_noingi.loc[index]):
        if type(v) == str:
            list_bad.extend(preprocessing(v))



list_bad = my_tokenizer_with_bigram(list_bad)

df_word_bad=df_word_bad(list_bad)
df_valuecounts_bad(df_word_bad)
