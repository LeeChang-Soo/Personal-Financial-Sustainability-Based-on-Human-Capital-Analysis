import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.optimize import minimize


def gen_human_capital(size, inital_hc, eta, mu_rf, period, hc_, mu_h, sigma_h):
    """

    :param size: monte carlo sample size
    :param inital_hc: initial labor income
    :param eta: calculated eta
    :param mu_rf: expected risk free asset return
    :param period: remained periods to retirement
    :param hc_: brownian labor income growth
    :param mu_h: expected labor income growth
    :param sigma_h: labor income standard deviation
    :return: human capital at input period
    """
    hc = np.ones([size, ]) * inital_hc

    hc_list = [hc]
    for i in range(period):
        hc_future = (hc * np.exp(mu_h + sigma_h * hc_[:, i])) * np.exp(-(i + 1) * (mu_rf + 0.04 + eta))
        hc_list.append(hc_future)
        hc = hc_future

    return np.sum(np.transpose(hc_list)[:, 2:], axis=1)


def get_maxutility_weights(inital_wealth, inital_hc, period, size, mu_rf, sigma_rf, mu_market, sigma_market, mu_h,
                           sigma_h, eta, rho, gamma):
    '''

    :param inital_wealth: inital financial wealth
    :param inital_hc: inital labor income
    :param period: remained periods to retirement
    :param size: monte carlo sample size
    :param mu_rf: expected risk free asset return
    :param sigma_rf: expected risk free standard deviation
    :param mu_market: expected market return
    :param sigma_market: expected market standard deviation
    :param mu_h: expected labor income growth
    :param sigma_h: expected labor income growth's standard deviation
    :param rho: correlation between human capital and market
    :param gamma: risk aversion tolerance
    :return: weights of maximum utility function
    '''
    eta = eta
    def objective_fun(weight, inital_wealth, inital_hc, period, size, mu_rf, mu_market, sigma_market, mu_h,
                      sigma_h, eta, rho, gamma):
        np.random.seed(period)

        market_ = stats.norm.rvs(size=(size, period + 1), loc=0, scale=1)
        brownian_ = stats.norm.rvs(size=(size, period + 1), loc=0, scale=1)
        hc_ = rho * market_ + np.sqrt(1 - rho ** 2) * brownian_

        wealth_sub = np.dot(
            np.array([np.exp(mu_market - 0.5 * (sigma_market ** 2) + sigma_market * market_[:, 0]), np.exp(mu_rf)]),
            weight)
        wealth_plus = (inital_wealth + inital_hc - inital_hc * 0.75) * wealth_sub

        if period == 0:
            hc_plus = 0
        else:
            hc_plus = gen_human_capital(size, inital_hc, eta, mu_rf, period, hc_, mu_h, sigma_h)

        u_ = ((wealth_plus + hc_plus) ** (1 - gamma)) / (1 - gamma)

        return 1 / np.mean(u_)

    weight = [np.ones([2]) / 2]
    cons = ({'type': 'ineq', 'fun': lambda weight: 1.0 - np.sum(weight)},
            {'type': 'ineq', 'fun': lambda weight: np.ones([2]) - weight[0]},)
    optimized = minimize(objective_fun, weight, (
        inital_wealth, inital_hc, period, size, mu_rf, sigma_rf, mu_market, sigma_market, mu_h, sigma_h, rho, gamma),
                         method='COBYLA', constraints=cons)
    if not optimized.success: raise BaseException(optimized.message)
    return optimized.x

