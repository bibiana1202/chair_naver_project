
from cgitb import text
from enum import EnumMeta
import enum
from importlib.resources import contents
from lib2to3.pgen2.pgen import ParserGenerator
from multiprocessing.context import _default_context
from sqlite3 import paramstyle
import string
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
file_name='kss_ingi_review'




def preprocessing(review):
    okt = Okt()
    # https://www.ranks.nl/stopwords/korean
    f = open(address_review+'stopwords_ingi.txt', encoding="utf-8")
    stop_words = f.read().split()
    
    g = open(address_review+'ingi_bad_dic.txt', encoding="utf-8")
    ingi_bad_dic = g.read().split()
    
    # 1. 한글 및 공백을 제외한 문자 모두 제거.
    review_text = re.sub("[^가-힣\\s]", "", review)
    # sub -> replace

    # 2. okt 객체를 활용해서 형태소 토큰화 + 품사 태깅(pos)
    # stem = 어간추출 -> 통일화
    word_review = okt.pos(review_text, stem=True)
    # 사전 단어 나올시 문장 자체를 삭제
    for (token,pos) in word_review:
        if token in ingi_bad_dic:   
            return ['']    
    
    # 노이즈 & 불용어 제거
    # _ 품사 자리 , pos 라고 잡아도 됨
    # _ : place holder. = 자리 지킴이
    word_review = [(token,pos) for token, pos in word_review if not token in stop_words and not token in ingi_bad_dic and len(token) > 1]
    
    # 명사, 동사, 형용사 추출
    word_review = [token for token, pos in word_review if pos in ['Noun', 'Adjective']]
    return word_review



def df_word_good(list1_good):
    df_word_good = pd.DataFrame(list1_good,columns=['word'])
    df_word_good.to_csv(path_or_buf=address_review+file_name+'_good_bigram'+'.csv',encoding = 'utf-8-sig')
    return df_word_good

def df_valuecounts_good(df_word_good):
    df_valuecounts_good=df_word_good['word'].value_counts()
    df_valuecounts_good.to_csv(path_or_buf=address_review+file_name+'_good_valuecount_bigram'+'.csv',encoding = 'utf-8-sig')

def my_tokenizer_with_bigram(list_tokens):
    list_d=[]
    for i in tqdm(range(len(list_tokens)-1),desc='bigram'):
        if(list_tokens[i]=='' or list_tokens[i+1]==''):
            continue
        list_d.append(' '.join(list_tokens[i:i+2]))
    return list_d


##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################################################################################################################################################################################################################

df_ingi = pd.read_csv(address_review+file_name+'.csv', header=0)
df_ingi.drop(df_ingi.columns[0],axis=1,inplace=True)

list_good=[]
for index in tqdm(range(len(df_ingi)),desc='문장'):
    for i,v in enumerate(df_ingi.loc[index]):
        if type(v) == str:
            list_good.extend(preprocessing(v))


list_good = my_tokenizer_with_bigram(list_good)

df_word_good=df_word_good(list_good)
df_valuecounts_good(df_word_good)