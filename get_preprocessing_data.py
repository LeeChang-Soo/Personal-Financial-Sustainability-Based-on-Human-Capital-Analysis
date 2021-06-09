import pandas as pd
import numpy as np


income_code_list = ["2102", "2134", "2136", " 2138", "2140", "2142", "2152", "2153", "2155", "2156",
                    "2157", "2158", "2159", "2160", "2182", "2183", "2184", "2185", "2186", "2187",
                    "2189", "2190", "2191"] #"2188"(축의, 조의금 제외)

# 1. 가구주인지 아닌지 확인
# 2.가구주면 h**2102(근로소득), h**2131(사회보험), h**2151(이전소득), h**2181(기타소득)
def get_personal_mask(personal_data):
    """

    :param personal_data: personal raw data
    :return: personal householder, educated filtered data
    """
    personal_data = personal_data.copy()

    householder_mask = (personal_data["0102"] == 10)
    householder_index = personal_data.index[householder_mask]

    edu_mask = (personal_data["0111"] == 1.0)
    edu_index = personal_data.index[edu_mask]

    return personal_data.iloc[householder_index & edu_index, :]


def get_edu(personal_masked_data):
    """

    :param personal_masked_data: after personal mask preprocessed data
    :return: after education preprocessed data
    """
    edu_data = personal_masked_data.copy()

    null_mask = (edu_data["0110"] < 5)
    high_mask = (edu_data["0110"] == 5)
    college_mask = (edu_data["0110"] == 6)
    univ_mask = (edu_data["0110"] == 7)
    grad_mask = (edu_data["0110"] > 7)

    edu_data.loc[null_mask, "0110"] = 0
    edu_data.loc[high_mask, "0110"] = 1
    edu_data.loc[college_mask, "0110"] = 2
    edu_data.loc[univ_mask, "0110"] = 3
    edu_data.loc[grad_mask, "0110"] = 3

    edu_index_mask = (edu_data["0110"] != 0)

    return edu_data.loc[edu_index_mask, :]


def get_sex(personal_educated_data):
    """

    :param personal_educated_data: after edu mask preprocessed data
    :return: after sex preprocessed data
    """
    sex_data = personal_educated_data.copy()

    #sex_mask = (sex_data["0101"] == 2)
    #sex_data.loc[sex_mask, "0101"] = 0
    sex_mask = (sex_data["0101"] != 2)
    #sex_data.loc[sex_mask, "0101"] = 0

    return sex_data.loc[sex_mask, :]#sex_data


def get_married(personal_sex_data):
    """

    :param personal_sex_data: after sex preprocessed data
    :return: after marriage preprocessed data
    """
    married_data = personal_sex_data.copy()

    married_mask = (married_data["5501"] == 2)

    married_data.loc[married_mask, "5501"] = 1
    married_data.loc[~married_mask, "5501"] = 0

    return married_data


def get_work(personal_married_data):
    """

    :param personal_married_data: after marriage preprocessed data
    :return: after working preprocessed data
    """
    work_data = personal_married_data.copy()

    work_mask = (work_data["jobtype"] == 1)
    work_data.loc[work_mask, "jobtype"] = "employ"
    work_data.loc[~work_mask, "jobtype"] = "unemploy"

    return work_data


def get_industry8(personal_worked_data, mid_industry_classification):
    """

    :param personal_worked_data: after working preprocessed data
    :param mid_industry_classification: data of middle class industry
    :return: after middle industry preprocessed data
    """
    industry_data = personal_worked_data.copy()
    mid_industry_classification = mid_industry_classification.copy().drop(0)

    for i in range(len(mid_industry_classification.columns)):
        mask_code = mid_industry_classification.iloc[:, i].dropna().values
        index_mask = industry_data["0330"].isin(mask_code)
        industry_data.loc[index_mask, "0330"] = mid_industry_classification.columns[i]

    return industry_data


def get_industry_sector(personal_midind_data, large_industry_classification):
    """

    :param personal_midind_data: after middle industry preprocessed data
    :param large_industry_classification: data of large class industry
    :return: after large industry preprocessed data
    """
    industry_data = personal_midind_data.copy()
    data_industry_kor = pd.DataFrame(large_industry_classification.columns, large_industry_classification.T.iloc[:, 0])
    large_industry_classification = large_industry_classification.copy().drop(0)

    for i in range(len(large_industry_classification.columns)):
        mask_code = large_industry_classification.iloc[:, i].dropna().values
        index_mask = industry_data["0330"].isin(mask_code)
        industry_data.loc[index_mask, "0330"] = data_industry_kor.iloc[i].name

    return industry_data.loc[industry_data["0330"].isin(data_industry_kor.index), :]


def get_fin_personal(personal_data, mid_industry_classification, large_industry_classification):
    """

    :param personal_data: personal raw data
    :param mid_industry_classification: data of middle class industry
    :param large_industry_classification: data of large class industry
    :return: total preprocessed personal data
    """
    temp_1 = get_personal_mask(personal_data)
    temp_2 = get_edu(temp_1)
    temp_3 = get_sex(temp_2)
    temp_4 = get_married(temp_3)
    temp_5 = get_work(temp_4)
    temp_6 = get_industry8(temp_5, mid_industry_classification)
    temp_7 = get_industry_sector(temp_6, large_industry_classification)

    fin_data = temp_7.loc[:, ["0101", "0110", "0107", "5501", "jobtype", "0330"]]
    fin_data.index = temp_7["hhid"]

    return fin_data


def get_income_data(personal_hhid, house_data):
    """

    :param personal_hhid: hhid from total preprocessed personal data(index)
    :param house_data: house raw data
    :return: total income of house
    """
    house_data = house_data.copy()
    house_data.index = house_data["hhid"]

    hhid_raw = house_data.loc[personal_hhid]
    income_data = hhid_raw.iloc[:, hhid_raw.columns.isin(income_code_list)].sum(axis=1)

    return income_data


def get_housing(house_data):
    """

    :param house_data: house raw data
    :return: after housing preprocessed data
    """
    housing_data = house_data.copy()

    housing_mask = (housing_data["1406"] != 1)
    housing_data.loc[housing_mask, "1406"] = 0

    return housing_data


def get_final_xvalue(house_data, fin_personal_data):
    """

    :param house_data: house raw data
    :param fin_personal_data: total preprocessed personal data
    :return: finally preprocessed x data
    """
    house_data = house_data.copy()
    house_data.index = house_data["hhid"]

    house_data = house_data.loc[fin_personal_data.index, :]

    temp_1 = get_housing(house_data)
    temp_2 = temp_1.loc[:, ["0150", "1406"]]

    return pd.concat([fin_personal_data, temp_2], axis=1)


def get_cpi_multi(cpi_data, data_degree_list):
    """

    :param cpi_data: cpi raw data
    :param data_degree_list: list of panel data degree
    :return: cpi multiple data
    """
    return (cpi_data[data_degree_list] / cpi_data[data_degree_list].values[-1]) ** -1


def get_final_yvalue(income_data, cpi_multiple):
    """

    :param income_data: total income of house
    :param cpi_multiple: cpi multiple
    :return: cpi adjusted income data
    """
    income_data = income_data.copy()
    income_data.name = "labor income"

    return income_data * cpi_multiple


def remove_novalue_index(cpi_adj_income):
    """

    :param cpi_adj_income: cpi adjusted income data
    :return: non-negative constraint data index
    """
    return cpi_adj_income[~(cpi_adj_income <= 0)].index



def get_total_data(cpi_adj_income, preprocessed_x_data):
    """

    :param cpi_adj_income: cpi adjusted income data
    :param preprocessed_x_data: finally preprocessed x data
    :return: x values dataframe, y values dataframe

    """
    nonegative_value_index = remove_novalue_index(cpi_adj_income)

    y = cpi_adj_income.loc[nonegative_value_index]
    x = preprocessed_x_data.loc[nonegative_value_index]

    return pd.concat([y, x], axis=1)


def get_agecut_data(data, start_age):
    """

    :param data: total preprocessed data
    :param start_age: start age
    :return: data with cutting age
    """
    data = data.copy()

    end = np.where(data["0107"] < 65)
    data = data.iloc[end]

    start = np.where(data["0107"] >= start_age)

    return data.iloc[start]