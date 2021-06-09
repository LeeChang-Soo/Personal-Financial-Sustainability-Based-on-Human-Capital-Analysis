import pandas as pd
import numpy as np
import statsmodels.regression.linear_model as sm


def get_reg_x(prepro_data):
    """

    :param prepro_data: preprocessed data(Edu, Edu & Industries, etc)
    :return: x data matrix
    """
    data = prepro_data.copy()

    intercept = pd.get_dummies(data["0101"])
    intercept.columns = ["intercept"]

    charactorized = data.loc[:, ["5501", "0150"]]
    charactorized.columns = ["marriage", "family_num"]

    x_matrix = pd.concat([intercept, charactorized], axis=1)
    x_matrix = pd.concat([x_matrix, pd.get_dummies(data["0107"])], axis=1)

    return x_matrix


def fe_regression_sol(prepro_data, summary_option=True):
    """

    :param prepro_data: preprocessed data(Edu, Edu & Industries, etc)
    :param summary_option: summary option
    :return: fixed effects regression results(parameters, pvalues)
    """
    x_matrix = get_reg_x(prepro_data)

    temp_sol = sm.OLS(np.log(prepro_data["labor income"].values), x_matrix)
    temp_result = temp_sol.fit()

    if summary_option is True:
        print(temp_result.summary())
    # print("-----------------------------------------------------------")
    return temp_result.params, np.round(temp_result.pvalues, 4)


def polynomial_matrix(age_data, degree):
    """

    :param age_data: age data vector
    :param degree: degrees of polynomials
    :return: x matrix for polynomials
    """
    x_matrix = np.zeros([len(age_data), degree + 1])
    x_matrix[:, 0] = 1

    columns_list = ["intercept"]
    for i in range(degree):
        x_matrix[:, i + 1] = age_data ** (i + 1) / 10 ** (i)
        columns_list.append("age^" + str(i + 1) + "/10^" + str(i))

    x_df = pd.DataFrame(x_matrix)
    x_df.columns = columns_list

    return x_df


def fitting_polynomial(fer_results, degree, summary_option=True):
    """

    :param fer_results: fixed effects regression results(parameters, pvalues)
    :param degree: degrees of polynomials
    :param summary_option: summary option
    :return: results of fitting polynomials value, params, p-values
    """
    dummy_coeff = fer_results

    temp_y = dummy_coeff[0][3:].values
    temp_x = dummy_coeff[0][3:].index.values

    #x_mat = np.zeros([len(temp_y), degree+1])
    #x_mat[:, 0] = 1

    #columns_list = ["intercept"]
    #for i in range(degree):
    #    x_mat[:, i+1] = temp_x**(i+1) / 10**(i)
    #    columns_list.append("age^"+str(i+1)+"/10^"+str(i))

    #x_df = pd.DataFrame(x_mat)
    #x_df.columns = columns_list
    x_df = polynomial_matrix(temp_x, degree)

    temp_sol = sm.OLS(temp_y, x_df)
    temp_result = temp_sol.fit()

    if summary_option is True:
        print(temp_result.summary())

    index_list = ["age_dummies("+str(degree)+"-order)", "fitted_polynomials("+str(degree)+"-order)"]
    return pd.DataFrame(np.array([temp_y, (x_df @ temp_result.params).values])+dummy_coeff[0][:3].sum(),
                        index=index_list, columns=temp_x).T, temp_result.params, temp_result.pvalues
