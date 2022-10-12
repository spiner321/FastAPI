# 모델 입력을 위한 전처리 함수

import mecab
import re

mecab = mecab.MeCab()

def mecab_tokenize(text):
    '''
    Mecab을 사용하여 tokenized text 반환
    '''
    return ' '.join(mecab.morphs(text))


def clean_etc_reg_ex(title):
    '''
    정규식을 통해 기타 공백과 기호, 숫자 등을 제거
    '''
    title = re.sub(r"[@%\\*=()/~#&\+á?\xc3\xa1\-\|\.\:\;\!\-\,\_\~\$\'\"]", "", title)  # remove punctuation
    title = re.sub(r"[∼%①②⑤⑪…→·]", "", title)
    title = re.sub(r"\d+", "", title)  # remove number
    title = re.sub(r"\s+", " ", title)  # remove extra space
    title = re.sub(r"<[^>]+>", "", title)  # remove Html tags
    title = re.sub(r"\s+", " ", title)  # remove spaces
    title = re.sub(r"^\s+", "", title)  # remove space from start
    title = re.sub(r"\s+$", "", title)  # remove space from the end
    title = re.sub("[一-龥]", "", title)
    
    return title


def slice_from_behind(text, num_of_chars):
    '''
    BERT의 최대 token 기준에 맞추기 위해, text를 slice
    '''
    
    return text[-num_of_chars:]


def preprocess(text):
    text = clean_etc_reg_ex(text)
    text = mecab_tokenize(text)
    
    return slice_from_behind(text, num_of_chars=500)