# -*- coding: utf-8 -*-
"""3단계_인기긍정.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r4EQkoaunoN6Bne8cUcGoFYNOfnXVdtT
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

df = pd.read_csv('/content/인기긍정_문장.csv')
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

# 긍정 속 불용어
stopwords_pos = ["의자",
"있다",
"이다",
"게이",
"아니다",
"문제",
"듭니",
"제닉스",
"만원",
"때문",
"에이",
"이번",
"이렇다",
"안나",
"드네",
"서도",
"울프",
"야하다",
"이제",
"가지",
"대로",
"기도",
"수도",
"보이",
"해도",
"치가",
"나중",
"나니",
"딱하다",
"에드",
"한지",
"신하",
"만큼",
"대요",
"어디",
"무용",
"위해",
"덕분",
"맘에듭니",
"대도",
"모든",
"요즘",
"도로",
"스럽다",
"잠깐",
"자마자",
"시디즈",
"어제",
"보시",
"이면",
"움직",
"분만",
"색도",
"용감",
"아침",
"여러",
"그게",
"구성은",
"만해",
"코로나",
"거나",
"인지",
"씨방",
"조이",
"일이",
"처럼",
"대한",
"아레나",
"분도",
"런가",
"판이",
"수고",
"몇개",
"다가",
"안보",
"월요일",
"중이",
"드릴",
"고해",
"일만",
"용의자",
"거기",
"사면",
"얘기",
"화요일",
"달동",
"는걸",
"토요일",
"해주시",
"은의자",
"인하다",
"빵빵",
"건가",
"군데",
"키티",
"지고",
"몇번",
"방이",
"등등",
"네이버",
"금요일",
"비도",
"된거",
"이구",
"달이",
"대해",
"이후",
"중역",
"삿는데",
"아마",
"다해",
"아예",
"듀오",
"여자친구",
"에쓰",
"전이",
"안해",
"보더",
"저번",
"자라",
"녀석",
"정이",
"가요",
"개월",
"추석",
"주신",
"부탁드리다",
"만하",
"대의",
"제네시스",
"면서",
"가형",
"루나",
"일요일",
"비애",
"그동안",
"자도",
"고양이",
"아보",
"잠도",
"파시",
"보지",
"쓰시",
"수요일",
"디테",
"레이",
"누우",
"수가",
"거림",
"애좀",
"건데",
"외로",
"신해",
"밉다",
"마침",
"려고",
"구가",
"앱코",
"블루",
"로서",
"이기",
"만약",
"목요일",
"파서",
"점도",
"사시",
"하진",
"비갑",
"쪼금",
"분안",
"대고",
"이상은",
"베리",
"용이",
"사자",
"모로",
"년전",
"곳도",
"능이",
"부터",
"오지",
"종종",
"읍니",
"지나",
"생기",
"도중",
"지도",
"사가",
"살껄",
"크리스마스",
"월일",
"주일",
"한텐",
"근대",
"요전",
"햇습니",
"어보",
"어찌",
"이서",
"이내",
"애가",
"작고",
"가나",
"헬로키티",
"그다지",
"기전",
"레알마드리드",
"감기",
"게다가",
"마냥",
"살때",
"대서",
"보임",
"신한",
"이나",
"사의",
"타이",
"자고",
"어쨌든",
"사라",
"래미",
"주심",
"하라",
"보구",
"년도",
"고정은",
"린다",
"직하다",
"로만",
"이즈",
"럭킹",
"로엠",
"작년",
"남아",
"지네",
"법도",
"립법",
"일수",
"힘좀",
"로고",
"로써",
"조만간",
"질도",
"부가",
"마자",
"어쨋",
"은감",
"올해",
"말로",
"깜놀",
"킬로",
"성도",
"레알",
"중아",
"안녕하다",
"담날",
"페라리",
"자로",
"타이탄",
"갠차다",
"만요",
"붙이",
"보아",
"사도",
"개중",
"꼽자",
"더니",
"네오",
"듯해",
"요하",
"천이",
"다음주",
"어어",
"걸렷",
"주네",
"주어",
"십만원",
"넷플릭스",
"리나",
"제스",
"번의",
"세용",
"요조",
"이케아",
"공휴일",
"저리",
"문후",
"도하",
"트리",
"저기",
"간정",
"다기",
"박아",
"나은",
"지난번",
"어딘가",
"하하",
"괜찬",
"우레",
"아영",
"아아",
"주정",
"무조",
"일간",
"래야",
"카톡",
"와중",
"이신",
"바보",
"주지",
"괜찬네",
"학적",
"데이",
"애초",
"살수",
"도편",
"명절",
"개사",
"제주도",
"드라마",
"정사",
"달뒤",
"괜찬아",
"다나",
"새해",
"하나요",
"그날",
"산이",
"줄알",
"차서",
"신의",
"라이언",
"천원",
"자네",
"리기",
"_는데",
"이빨",
"발라",
"끼리",
"리가",
"이예",
"지면",
"부디",
"잘만",
"조음",
"일루",
"독도",
"저런",
"유_",
"성은",
"아시",
"한장",
"일차",
"오니",
"라서",
"_혀",
"베스",
"상보",
"때매",
"판도",
"요강",
"달래",
"완젼",
"훨신",
"오우",
"위자",
"여주면",
"레고",
"괜춘",
"체로키",
"롯데",
"닉스",
"나위",
"가기",
"나기",
"이자",
"듯이",
"거지",
"송해",
"대치",
"바_는데",
"이드",
"싸이",
"삿어",
"부러",
"먹음",
"쿠팡",
"상이",
"치도",
"요도",
"해해",
"_아",
"우유",
"비굿",
"아연",
"이러하다",
"헛도",
"설날",
"부의",
"어디가",
"역쉬",
"간이",
"나가시",
"프라스",
"이왕이면",
"요키",
"조리",
"다다",
"취하",
"음날",
"평보",
"대면",
"이안",
"두운",
"타고",
"로켓",
"로라",
"추강",
"비지",
"보태",
"_오",
"가안",
"일해",
"힐때",
"딸기",
"도깨비",
"로안",
"위너",
"평일",
"요기",
"무방",
"일지",
"결재",
"보라",
"아라하",
"분동",
"플스",
"고하",
"키도",
"주소",
"쇼핑몰",
"대반",
"래서",
"페이",
"용돈",
"구나",
"엇어",
"금일",
"지금껏",
"듭니당",
"힐수",
"별거",
"달후",
"문해",
"이보",
"안타",
"갈수록",
"오브",
"할_",
"어린이날",
"잔고",
"도도",
"키크",
"시국",
"발바",
"오오",
"하내",
"요요",
"파악",
"삿다",
"립하",
"병원",
"바지",
"마블",
"유툽",
"오버",
"던데",
"삼일",
"적도",
"차요",
"매하",
"도해",
"의하다",
"렵니",
"인제",
"돌이",
"코스트코",
"연말",
"이지",
"취할",
"어우",
"제니스",
"어요",
"유튜버",
"습니",
"간다",
"비슷",
"구해",
"가원",
"요다음",
"여서",
"자임",
"마나",
"제규",
"카이저",
"이오",
"내년",
"마넌",
"부방",
"돈좀",
"로젠택배",
"도크",
"가가",
"가시",
"글구",
"위메프",
"들보",
"정부",
"홈쇼핑",
"나진",
"수많다",
"마이",
"서하",
"인터파크",
"대인",
"과제",
"고함",
"대만",
"시디",
"주니",
"듬니",
"빨랏",
"드네용",
"역다",
"모래",
"안고",
"서프라이즈",
"나라",
"피고",
"거렸",
"난후",
"어서",
"고합",
"사드",
"자형",
"티자",
"엇네",
"아쥬",
"가나다",
"에노",
"메시",
"하리",
"조정은",
"엇습",
"쓰는덴",
"지구",
"이란",
"빌라",
"어피",
"쏙듭니",
"가라",
"월욜",
"조일",
"뒤늦다",
"_문",
"졸음",
"여야",
"구라",
"요게",
"지난주",
"슬슬",
"성형",
"정이안",
"전역",
"눌리",
"진과",
"배그",
"무크",
"요한",
"빅스",
"왓는데",
"후시",
"괜츈",
"날때",
"지라",
"에두",
"도아",
"대구",
"리지",
"드니",
"마안",
"이듭",
"안제",
"리도",
"편햐",
"송전",
"이주",
"어느덧다",
"드렷",
"거제",
"원대",
"구름",
"시경",
"랍니",
"여진",
"왜인",
"금욜",
"휴일",
"지옥",
"나선",
"무쟈",
"쪼매",
"서나",
"갈수",
"다자",
"클리",
"라며",
"놨는데",
"유심",
"재배",
"사나",
"새재",
"취할때",
"머진",
"요나",
"덕소",
"차차",
"주더",
"개도",
"알짝",
"비주",
"여요",
"더욱이",
"대감",
"휘거",
"졸리",
"중요시",
"옥션",
"비제",
"절기",
"장날",
"태풍",
"프랑스",
"마일",
"간반",
"칠이",
"조마조마하다",
"더크",
"로엠가구",
"비적",
"적지",
"차이나",
"찰것",
"립니",
"익일",
"장재",
"등각",
"셧으",
"가야",
"딩기",
"프레",
"해주",
"거여",
"장마",
"클릭",
"시구",
"클라인",
"_던",
"더더",
"조아연",
"은줄",
"달전",
"두시",
"요것",
"거릴",
"어째",
"쉬_",
"루루",
"시나",
"배송지",
"요정",
"만적",
"입력",
"어케",
"껀데",
"할껄",
"서하면",
"완조",
"치과",
"원주고",
"은하",
"일상생활",
"아우",
"눌린",
"이이",
"한국",
"라마",
"바사",
"니나",
"벤틀리",
"빡셉니",
"해커",
"밍용",
"악세다",
"갈릴",
"밀러",
"난건",
"죄송스럽다",
"유투",
"공홈",
"비트",
"요타",
"돌리시",
"왜냐면",
"꼽으",
"만천원",
"폭설",
"나가요",
"더러",
"나나",
"데넘",
"에디",
"방도",
"가해",
"절때",
"노노",
"빼기",
"화장",
"고저",
"거립니",
"팔면",
"임용",
"일어나지",
"자모",
"중하",
"하규",
"치인",
"쪼으",
"년차",
"어진",
"신건",
"부와",
"지마켓",
"가트",
"엇음",
"카카오",
"일인",
"따리",
"에이펙",
"서요",
"갑인",
"환자",
"점심시간",
"요원",
"시보",
"저서",
"동서",
"컬리",
"우리나라",
"국민",
"싱하",
"김포",
"만가",
"비쥬",
"진보면",
"제껀",
"딜로",
"성용",
"실으",
"디쟌",
"아앙",
"_다",
"훌쩍",
"담배",
"요안",
"_니",
"건담",
"렌지",
"그로",
"로움",
"안산",
"놀랏",
"커브",
"구오",
"번하다",
"친하다",
"가편",
"이아주",
"달도",
"무니",
"리보",
"소린",
"고여",
"구래",
"오자",
"아이언맨",
"바자",
"차카",
"니아",
"포옥",
"푸신",
"괜춘합니",
"스마",
"햇던",
"이지나",
"잘되지",
"영업일",
"민하",
"지하",
"반년",
"생상",
"고치",
"바르샤",
"기우",
"지게",
"안넘",
"줄평",
"판하",
"품사",
"해치",
"따름",
"당근",
"목하",
"써_는데",
"통운",
"마켓",
"오라",
"너므",
"바로다",
"부다",
"엑스",
"다이아",
"귀차니즘",
"놨네",
"요팔",
"지스",
"후의",
"베이",
"쫌더",
"저건",
"선지",
"바_",
"느꼇습니",
"서핑",
"난생",
"고서",
"주전",
"적임",
"마춤",
"햇음",
"_찮네",
"장시",
"전의",
"개월전",
"_히",
"어쩌",
"대지",
"내장",
"인사",
"까치",
"가의",
"나열",
"번은",
"로나",
"토크",
"물이",
"마리",
"시즈",
"시몬",
"라꾸",
"다그",
"유로",
"디아",
"블프",
"쇠라",
"_으",
"그간",
"번가",
"모나",
"하나라",
"렛잇고",
"빅사",
"의치",
"두기",
"부랴부랴",
"클레",
"더라도",
"쓰렵니",
"애도",
"애로",
"좋아욤",
"신지",
"가작",
"타도",
"유공",
"토욜",
"착상",
"밀림",
"작시",
"해먹",
"한상태",
"이중",
"마약",
"해지",
"보심",
"거도",
"엉엉",
"안듭니",
"왓습니",
"서울",
"증말",
"어도",
"열흘",
"더삼",
"루지",
"재포",
"없엇구",
"버거",
"듀백",
"도나",
"등대",
"알람",
"의전",
"의뢰",
"볼땐",
"일룸",
"조힙",
"장제",
"과극",
"드내",
"삿던",
"리오네",
"_아",
"인걸",
"무오",
"대여",
"이요",
"내지",
"습시",
"안드",
"비론",
"햇구",
"발의",
"생것",
"완죤",
"괜찬음",
"마누라",
"이산",
"_어져",
"크시",
"외한",
"꼽기",
"은애",
"또살",
"방인",
"고골",
"지망",
"장도",
"나마",
"_습니",
"인천",
"비값",
"조항",
"만조",
"할부",
"삐죽다",
"자의",
"춘해",
"갠찮",
"스티",
"키카",
"빙의",
"괜춘해",
"그이",
"_곤",
"죠아",
"용제",
"듭니다",
"대야",
"바르셀로나",
"로우",
"여조",
"의뢰인",
"고고",
"급니",
"핑쿠핑쿠",
"엄니",
"후원",
]

rev

all = []
for i in rev:
    pos_sen = []
    for j in i:
        pos_words = []
        for word, pos in j:
            if (pos == 'Noun' or pos == 'Adjective') and len(word) >= 2 and not word in stopwords_pos:
                    pos_words.append([word, pos])
        pos_sen.append(pos_words)
    all.append(pos_sen)
all

# 긍정 속 부정어 - 부정 사전

neg_words_lst = ["어렵다",
"소음",
"힘들다",
"불편하다",
"아쉽다",
"냄새",
"다만",
"약간",
"아프다",
"살짝",
"안되다",
"무겁다",
"단점",
"불량",
"딱딱하다",
"비싸다",
"무거워",
"하자",
"별로",
"나쁘다",
"덥다",
"파손",
"약하다",
"힘드다",
"안좋다",
"고생",
"심하다",
"고장",
"삐걱",
"불안하다",
"좁다",
"뻑뻑",
"무리",
"느리다",
"귀찮다",
"잘못",
"어려움",
"반품",
"부족하다",
"추하다",
"당황",
"사고",
"부담",
"이상하다",
"부실하다",
"기스",
"싸구려",
"유격",
"흠집",
"애매하다",
"번거롭다",
"아깝다",
"헷갈리다",
"스크래치",
"불만",
"필요없다",
"자국",
"누락",
"불편",
"별하나",
"쓰리다",
"겨우",
"피곤하다",
"실밥",
"통증",
"환기",
"싫다",
"덜렁",
"나머진",
"빡빡",
"버겁다",
"얼룩",
"일부",
"더럽다",
"불량품",
"쓰레기",
"그닥",
"억지로",
"스크레치",
"속상하다",
"불구",
"날카롭다",
"거려",
"짜증나다",
"상처",
"무거",
"짜증",
"헐렁하다",
"의심",
"중고",
"헐겁다",
"가루",
"차라리",
"실망",
"답답하다",
"문제점",
"실망하다",
"후회되다",
"흔적",
"지연",
"지저분하다",
"녹슨",
"불친절하다",
"빡치다",
"잔기스",
"싫어하다",
"감수",
"염려",
"군데군데",
"스트레스",
"엉망",
"불안정하다",
"안타깝다",
"난감하다",
"천하다",
"사소하다",
"촌스럽다",
"박살",
"부족",
"뻐근하다",
"힘없다",
"거짓말",
"오기",
"부실",
"탈취",
"미끄럽다",
"한숨",
"불만족",
"의아",
"아다리",
"티나",
"어중간하다",
"구부정하다",
"강제",
"느슨하다",
"불쾌하다",
"야마",
"어지간하다",
"훼손",
"이염",
"뻘뻘",
"싼마이",
"구리다",
"실패하다",
"찝찝하다",
"헤져",
"불가능",
"뻣뻣하다",
"드럽다",
"불량하다",
"분하다",
"이격",
"반면",
"물렁하다",
"진땀",
"당하다",
"헛돌",
"일일이",
"별루",
"난해하다",
"찜찜하다",
"부직포",
"미묘하다",
"식겁하다",
"불가하다",
"마모",
"조잡하다",
"심각하다",
"안드네",
"불평",
"어설프다",
"끼익끼익",
"함정",
"최악",
"끼익",
"질질",
"헤메",
"안쓰럽다",
"너덜너덜하다",
"피로하다",
"망하다",
"쓸데없다",
"힘겹다",
"에러",
"빡셈",
"낭패",
"무언가",
"울퉁불퉁하다",
"혼동",
"무식하다",
"곰팡이",
"어이없다",
"배겨",
"타카",
"낑기다",
"우여곡절",
"혼란",
"칼집",
"시끄럽다",
"부자연스럽다",
"따갑다",
"낭비",
"덜덜",
"도대체",
"뚝뚝",
"잡음",
"저림",
"따위",
"그지같다",
"착오",
"자칫",
"석유",
"기스나",
"유발",
"황당하다",
"지체",
"고통",
"걸레",
"붕뜨",
"풀림",
"빈약하다",
"뽀각",
"댓글알바",
"글쎄요",
"우수수",
"곤란하다",
"중상",
"박하다",
"악취",
"삐거덕",
"쪼가리",
"칙칙하다",
"디다",
"헛도네",
"베겨",
"패임",
"개판",
"말썽",
"반송",
"애먹엇네",
"거부",
"계륵",
"크랙",
"고약하다",
"탁하다",
"미흡",
"경고",
"쇳가루",
"바가지",
"피해",
"무지막지",
"알갱이",
"더군다나",
"혈압",
"긁힌",
"혼돈",
"폐기",
"스크레",
"찌꺼기",
"짝짝",
"에바",
"배김",
"덕거려",
"민망하다",
"축축하다",
"보풀",
"뿌셔져",
"범벅"
]

# all = []
# for i in rev:
#     # pos_sen = []
#     for j in i:
#         pos_words = []
#         for word, pos in j:
#             if (pos == 'Noun' or pos == 'Adjective') and len(word) >= 2 and not word in stopwords_pos:
#                     pos_words.append([word, pos])
#     all.append(pos_words)
# all

# two_meanings_rev = []
# for rev in all:
#     for sen in rev:
#         neg_contained = []
#         for token in sen :
#             if token[0] in neg_words_lst:
#                 neg_contained.append(sen)
#                 break
#             else:
#                 continue
#     two_meanings_rev.extend(neg_contained)


# two_meanings_rev

# two_meanings_rev = []
# for rev in all:
#     for sen in rev:
#         neg_contained = []
#         for token in sen :
#             if token[0] in neg_words_lst:
#                 neg_contained.append(sen)
#                 break
#             else:
#                 continue
#     two_meanings_rev.extend(neg_contained)


# two_meanings_rev

two_mean_sen = []
for review in all :
    for sen in review:
        neg_contain =[]
        for token in sen :
            if not token[0] in neg_words_lst:
                continue 
            else:
                neg_contain.append(sen)
                break
        two_mean_sen.extend(neg_contain)
two_mean_sen

len(two_mean_sen)

within_sen_pos = []
for sen in two_mean_sen:
    for token in sen :
        if not token[0] in stopwords_pos and not token[0] in neg_words_lst:  # 불용어도 아니고 부정사전에도 없는 단어 -> 순수 긍정
            within_sen_pos.append(token)
within_sen_pos

# 불용어, 부정 단어 없는 긍정키워드  -> 추가해서 빈도 세기 
add_pos = []

for word in within_sen_pos:
    add_pos.append(word[0])
len(add_pos)

import pandas as pd
pos_B = pd.read_csv('/content/긍정키워드_B_규인.csv', encoding = 'CP949')
pos_B_lst = list(pos_B['긍정_B'])
len(pos_B_lst)

pos_B_lst.extend(add_pos)
len(pos_B_lst)

from collections import Counter
c = Counter(pos_B_lst)
positive_count_C = c.most_common()
positive_count_C
# dic_cnt = dict(c)
# dic_cnt

dic_pos_C = {'키워드':[], 
       '빈도':[]}
for i in positive_count_C:
    dic_pos_C['키워드'].append(i[0])
    dic_pos_C['빈도'].append(i[1])
dic_pos_C

df_pos_C = pd.DataFrame(dic_pos_C)
df_pos_C

df_pos_C.to_csv('인기긍정키워드_C단계_효진.csv', encoding='cp949')

