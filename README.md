# Personal-Financial-Sustainability-Based-on-Human-Capital-Analysis
개인의 특성 데이터와 기대효용 최적화 기법을 활용한 생애주기별 자산관리  논문

논문 링크 : https://www.mdpi.com/2071-1050/13/5/2700/htm

## 사용 데이터 ( data file )
KLIPS(한국노동패널)데이터의 개인데이터와 가구데이터, 거시경제 데이터인 CPI데이터와 산업군별 수익률, 국내와 해외의 국채데이터 등 

## Glide_path 파이썬 코드
은퇴시점이 다가옴에 따라 위험자산(주식)의 비중을 점차 줄이고 안전자산(채권)의 비중을 점차 늘리는 모습을 일컫는 말로, 점차 줄어드는 위험자산(주 식)비중이 상공에서 글라이더(Glider)가 점차 아래로 착륙하는 과정(Path)과 비슷하다고 하여 일컫는 단어
이러한 Glide_path를 구현하기 위한 코드로 Calibration_Labor_Income으로 부터 산출된 Input 값을 활용한다.

## Calibration_Labor_Income 파이썬 코드
논문의 핵심인 인적자본 추정을 위해 KLIPS데이터의 임금과 개인특성 데이터를 활용해 인적자본을 추산하며
Fixed effect모형과 비슷한 효과를 내기 위해 학력별로 학습셋을 분리하여 회귀분석을 진행하였다. 
또한 나이를 다항회귀(Polynomial regressions)함수로 고려하여 생애주기별 인적자본의 추이를 파악한다.

## get_raw_data 파이썬 코드
KLIPS(한국노동패널)의 raw 데이터를 논문 작성에 필요한 부분만 가져오는 코드

## get_preprocessing_data 파이썬 코드
개인 특성을 나타내는 변수와 인적자본 산출을 위한 소비자 물가, 산업군 return 데이터 등을 각각 전처리하는 코드

## analysis_method 파이썬 코드
인적자본을 산출하기 위한 코드이며, 각 함수는 아래의 설명과 같다

def get_reg_x(prepro_data): 회귀분석에 필요한 x변수를 가공하는 코드

def fe_regression_sol(prepro_data, summary_option=True): x변수를 활용하여 y변수인 인적자본을 회귀분석하는 과정

def polynomial_matrix(age_data, degree): 나이변수를 활용하여 다항회귀분석을 진행 ( 생애주기별 인적자본을 추산하기 위해 )
