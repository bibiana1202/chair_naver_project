
import kss
import pandas as pd
import re
from tqdm import tqdm


def kss_review(list_review,filename):
  list_content = []
  for i in range(len(list_review)):
      if list_review["score"][i] <=3:
          list_content.append(list_review["content"][i])

  l_contentn = []
  for i in range(len(list_content)):
      content_textn = re.sub("[^가-힣\\s]", "", list_content[i])
      l_contentn.append(content_textn)
  
  kss_review = []

  for i in tqdm(range(len(l_contentn))):
    kss_review.append(kss.split_sentences(l_contentn[i]))

  df_kss_sentence = pd.DataFrame(kss_review)
  df_kss_sentence.to_csv("kss_"+filename+"_review.csv", encoding='utf-8-sig')

###########################################################################################
###########################################################################################

address_review='/Volumes/GoogleDrive/내 드라이브/'

file_name_ingi='df_ingi_review'
file_name_noingi='df_noingi_review'


list_noingi_review = pd.read_csv(file_name_noingi+'.csv')
list_ingi_review = pd.read_csv(file_name_ingi+'.csv')


kss_review(list_noingi_review,'noingi')
kss_review(list_ingi_review,'ingi')
