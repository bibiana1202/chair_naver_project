# -*- coding: utf-8 -*-
"""3단계_비인기부정.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YQiiiJoQ7JB12-zF1lnGAdwQyKEO9KLF
"""

!pip install konlpy

from konlpy.tag import Okt # komoran, hannanum, kkma, mecab
#konlpy의 tag 파일 안에 Okt라는 class만 import
#konlpy 안에 tag 파일 존재 -> 다른 선상에 존재 
import os

import numpy as np
import pandas as pd

from datetime import datetime
import json
import re


from tqdm.notebook import tqdm

df = pd.read_csv('/content/비인기부정_문장단위.csv')
df

df = df.transpose()
df.rename(columns = df.iloc[0], inplace = True)
df= df.drop(df.index[0])

df_list = []
for i in range(len(df.columns)):
  lista = []
  for j in range(len(df)):
    
    if not pd.isna(df[df.columns[i]][j]):
      lista.append(df[df.columns[i]][j])
  df_list.append(lista)

df_list

okt = Okt()
rev = []
for i in df_list:
    sentence = []
    for j in i:
        sentence.append(okt.pos(j, stem = True))
    rev.append(sentence)
rev

len(rev)

# 부정 속 불용어 

stopwords_neg = ["의자",
"제품",
"오다",
"이다",
"보다",
"배송",
"쓸다",
"만원",
"해주다",
"가다",
"짜다",
"차다",
"나다",
"치다"
]
# 부정 리뷰 속 긍정 단어 - 긍정사전 
pos_words_lst = ["좋다",
"만족하다",
"괜찮다",
"편하다"
]

all = []
for i in rev:
    neg_sen = []
    for j in i:
        neg_words = []
        for word, pos in j:
            if (pos == 'Noun' or pos == 'Adjective') and len(word) >= 2 and not word in stopwords_neg:
                    neg_words.append([word, pos])
        neg_sen.append(neg_words)
    all.append(neg_sen)
all

two_mean_sen = []
for review in all :
    for sen in review:
        pos_contain =[]
        for token in sen :
            if not token[0] in pos_words_lst:
                continue 
            else:
                pos_contain.append(sen)
                break
        two_mean_sen.extend(pos_contain)
two_mean_sen

len(two_mean_sen)

within_sen_neg = []
for sen in two_mean_sen:
    for token in sen :
        if not token[0] in stopwords_neg and not token[0] in pos_words_lst:  # 불용어도 아니고 긍정사전에도 없는 단어 -> 순수 부정
            within_sen_neg.append(token)
within_sen_neg

# 불용어, 긍정 단어 없는 부정키워드  -> 추가해서 빈도 세기 
add_neg = []

for word in within_sen_neg:
    add_neg.append(word[0])
add_neg

# 문장 단위 삭제된 부정어 리스트에 부정어만 뽑은거 추가하기 
import pandas as pd
neg_B = pd.read_excel('/content/B_비인기부정키워드.xlsx')
neg_B_lst = list(neg_B['키워드'])
neg_B_lst

neg_B_lst.extend(add_neg)
len(neg_B_lst)

from collections import Counter
c = Counter(neg_B_lst)
negative_count_C = c.most_common()
negative_count_C

dic_neg_C = {'키워드':[], 
       '빈도':[]}
for i in negative_count_C:
    dic_neg_C['키워드'].append(i[0])
    dic_neg_C['빈도'].append(i[1])
dic_neg_C

df_neg_C = pd.DataFrame(dic_neg_C)
df_neg_C

df_neg_C.to_csv('비인기부정키워드_C단계_효진.csv', encoding='cp949')

