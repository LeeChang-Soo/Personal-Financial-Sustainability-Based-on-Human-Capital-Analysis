# Personal-Financial-Sustainability-Based-on-Human-Capital-Analysis
개인의 특성 데이터와 기대효용 최적화 기법을 활용한 생애주기별 자산관리  논문

논문 링크 : https://www.mdpi.com/2071-1050/13/5/2700/htm

## Glide_path 파이썬 코드

## Calibration_Labor_Income 파이썬 코드

## get_raw_data 파이썬 코드
KLIPS(한국노동패널)의 raw 데이터를 논문 작성에 필요한 부분만 가져오는 코드

## get_preprocessing_data 파이썬 코드
개인 특성을 나타내는 변수와 인적자본 산출을 위한 소비자 물가, 산업군 return 데이터 등을 각각 전처리하는 코드
def get_personal_mask(personal_data):
def get_edu(personal_masked_data):
def get_sex(personal_educated_data):
def get_married(personal_sex_data):
def get_work(personal_married_data):
def get_industry8(personal_worked_data, mid_industry_classification):
def get_industry_sector(personal_midind_data, large_industry_classification):
def get_income_data(personal_hhid, house_data):
def get_housing(house_data):
def get_final_xvalue(house_data, fin_personal_data):
def get_cpi_multi(cpi_data, data_degree_list):
def get_final_yvalue(income_data, cpi_multiple):
def remove_novalue_index(cpi_adj_income):
def get_total_data(cpi_adj_income, preprocessed_x_data):
def get_agecut_data(data, start_age):
## analysis_method 파이썬 코드
