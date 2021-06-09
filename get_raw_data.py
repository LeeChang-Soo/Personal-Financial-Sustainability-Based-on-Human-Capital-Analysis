import pandas as pd


pv_list = ["0102", "1701", "1702", "0111", "0330", "0331", "0332", "0333", "0101", "0107", "0110", "5501"]
#["0102"(가구주와의 관계), "1701"(근로소득 유무), "1702"(총 연간근로소득), "0111"(학력졸업여부), "0330"(업종8차),
# "0331"(업종9차), "0332"(직종8차), "0333"(직종9차), "0101"(성별), "0107"(만나이), "0110"(학력학교), "5501"(혼인상태)]
hv_list = ["0150", "1406", "2102", "2134", "2136", " 2138", "2140", "2142", "2152", "2153", "2155",
           "2156", "2157", "2158", "2159", "2160", "2182", "2183", "2184", "2185", "2186", "2187",
           "2189", "2190", "2191"]
#["0150"(가구원수), "1406"(입주형태), 나머지는 각종 소득


def make_pv_list(pv_list, degree):
    """

    :param pv_list: personal value code list
    :param degree: N degree of panel data
    :return: personal list of degrees, personal value list
    """
    pv_list_new = []
    for i in pv_list:
        temp_value = "p" + degree + i
        pv_list_new.append(temp_value)

    pv_list_new.append("hhid" + degree)
    pv_list_new.append("jobtype")
    pv_list_new.append("pid")

    pv_list.append("hhid")
    pv_list.append("jobtype")
    pv_list.append("pid")

    return pd.Index(pv_list_new), pd.Index(pv_list)


def get_pv_data(data, pv_list, degree):
    """

    :param data: raw data of personal data
    :param pv_list: personal value code list
    :param degree: N degree of panel data
    :return: factor sliced personal data
    """
    pv_list_index, pv_columns = make_pv_list(pv_list, degree)
    columns_value = pv_list_index[pv_list_index.isin(data.columns[data.columns.isin(pv_list_index)])]
    data_pv = data.loc[:, columns_value]

    data_pv.columns = pv_columns[pv_list_index.isin(data_pv.columns)]
    #data_pv.index = data_pv["hhid"]

    return data_pv


def make_hv_list(hv_list, degree):
    """

    :param hv_list: house value code list
    :param degree: N degree of panel daa
    :return: house list of degrees, house value list
    """
    hv_list_new = []
    for i in hv_list:
        temp_value = "h" + degree + i
        hv_list_new.append(temp_value)

    hv_list_new.append("hhid" + degree)
    hv_list_new.append("htype" + degree)

    hv_list.append("hhid")
    hv_list.append("htype")

    return pd.Index(hv_list_new), pd.Index(hv_list)


def get_hv_data(data, hv_list, degree):
    """

    :param data: raw data of house data
    :param hv_list: house value code list
    :param degree: N degree of panel daa
    :return: factor sliced house data
    """
    hv_list_index, hv_columns = make_hv_list(hv_list, degree)
    columns_value = hv_list_index[hv_list_index.isin(data.columns[data.columns.isin(hv_list_index)])]
    data_hv = data.loc[:, columns_value]

    data_hv.columns = hv_columns[hv_list_index.isin(data_hv.columns)]
    #data_hv.index = data_hv["hhid"]

    return data_hv

