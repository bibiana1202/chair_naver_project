from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np
import pandas as pd



### 파일 불러오기 (파일 하니씩 읽어서 아래코드 실행)

# df=pd.read_excel('A_인기긍정_최종.xlsx')
# df=pd.read_excel('B_인기긍정_최종.xlsx')
# df=pd.read_csv('인기긍정키워드_C단계_효진.csv', encoding="cp949")
# df=pd.read_excel('인기_긍정_순수_C.xlsx' )     
# df=pd.read_excel('인기긍정_바이그램_최종.xlsx')
# df=pd.read_excel('인기긍정_3-gram_최종.xlsx')

# df=pd.read_excel('비인기_부정_순수_A.xlsx')
# df=pd.read_excel('비인기_부정_순수_B.xlsx')
# df=pd.read_csv('비인기부정키워드_C단계_효진.csv', encoding="cp949")
# df=pd.read_excel('비인기_부정_순수_C.xlsx')
# df=pd.read_excel('비인기_부정_bigram.xlsx')
df=pd.read_excel('비인기_부정_trigram.xlsx')


# column이름 별로 불러오기
a = df["키워드"]
b = df["빈도"]


# 딕셔너리 형태로 변환하기
dic = {}

for i,j in zip(a,b):
    dic["{}".format(i)] = j



# 워드 클라우드로 만들기
img = Image.open('cb_2.jpg')  # 게이밍 의자모양 이미지 파일
img_array = np.array(img)

wc = WordCloud(font_path='malgun', background_color='white', width=1000, height=1000 ,max_words=100, max_font_size=300, mask=img_array)
gen = wc.generate_from_frequencies(dic)

wc.to_file("3gram-비인기.png") # 이미지 파일 만들기
plt.figure()
plt.imshow(gen)