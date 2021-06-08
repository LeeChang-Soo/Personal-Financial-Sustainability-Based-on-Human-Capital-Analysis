# Personal-Financial-Sustainability-Based-on-Human-Capital-Analysis
개인의 특성 데이터와 기대효용 최적화 기법을 활용한 생애주기별 자산관리  논문

논문 링크 : https://www.mdpi.com/2071-1050/13/5/2700/htm

## Glide_path 파이썬 코드

## Calibration_Labor_Income 파이썬 코드

## get_raw_data 파이썬 코드
KLIPS(한국노동패널)의 raw 데이터를 논문 작성에 필요한 부분만 가져오는 코드

## get_preprocessing_data 파이썬 코드
개인 특성을 나타내는 변수와 인적자본 산출을 위한 소비자 물가, 산업군 return 데이터 등을 각각 전처리하는 코드

## analysis_method 파이썬 코드
인적자본을 산출하기 위한 코드이며, 각 함수는 아래의 설명과 같다

def get_reg_x(prepro_data): 회귀분석에 필요한 x변수를 가공하는 코드

def fe_regression_sol(prepro_data, summary_option=True): x변수를 활용하여 y변수인 인적자본을 회귀분석하는 과정

def polynomial_matrix(age_data, degree): 나이변수를 활용하여 다항회귀분석을 진행 ( 생애주기별 인적자본을 추산하기 위해 )
