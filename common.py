# Define general information common to all analyses

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import scipy.stats as stats

environments = ['LB', 'M9-Glucose', 'Urine', 'Colon']
backgrounds  = ['MG1655', 'PB2', 'PB5', 'OLC809', 'PB6', 'PB10', 'PB1', 'PB4', 'OLC682', 'OLC969', 'PB13', 'PB15']
mutations    = ['gyrA_S83L_D87N', 'gyrB_D426N', 'marR_R77H', 'rpoB_H526Y', 'rpoB_S531L', 'rpsL_K43R', 'rpsL_K43T']

n_envs        = len(environments)
n_backgrounds = len(backgrounds)
n_mutations   = len(mutations)
n_env_pairs = n_envs*(n_envs-1)//2

COLORS_BAR = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

COLORS = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#999999"]
COLORS_ENV = [COLORS[0], COLORS[1], COLORS[-2], COLORS[-1]]

n_samples = 10000
recalculate = True
replot = True

np.random.seed(3618587536)

def p_value(value, test, error):
    zscore = np.abs((value - test)/error)
    return 1 - stats.norm.cdf(zscore)

def flatten_and_clean_nans(lst, lst2=None):
    if lst2 is None:
        lst = lst.flatten()
        eliminate = np.argwhere(np.isnan(lst))
        return np.delete(lst, eliminate)
    else:
        lst = lst.flatten()
        eliminate = np.argwhere(np.isnan(lst))
        return np.delete(lst, eliminate), np.delete(lst2.flatten(), eliminate)

def pearson_correlation_coefficient(lst1, lst2):
    return np.corrcoef( np.array( [flatten_and_clean_nans(lst1), flatten_and_clean_nans(lst2)] ) )[0,1]


def linear_fit(x, y, color, alpha=0.1, ax=plt):
    # Statistics
    n = y.size                                            # number of observations
    m = 2                                                 # number of parameters
    dof = n - m                                           # degrees of freedom
    t = stats.t.ppf(alpha/2, n - m)                       # used for CI and PI bands

    fit = np.polyfit(x, y, 1)
    p = np.poly1d(fit)

    xp = np.linspace(x.min(), x.max(), 100)
    ax.plot(xp, p(xp), '--', color=color)

    #https://stats.stackexchange.com/questions/101318/understanding-shape-and-calculation-of-confidence-bands-in-linear-regression
    #www2.stat.duke.edu/~tjl13/s101/slides/unit6lec3H.pdf
    sYgX = np.zeros(len(xp))
    for j, xx in enumerate(xp):
        for i in range(n):
            sYgX[j] += (y[i] - p(xx))**2
    sYgX = np.sqrt(sYgX/(n-2))

    mx = np.mean(x)
    sY = sYgX * np.sqrt(1/n + (xp - mx)**2/np.sum((x - mx)**2))

    ax.fill_between(xp, p(xp) - t*sY, p(xp) + t*sY, alpha=0.2, color=color)

def format_p_value(p):
    if p < 1e-10:
        return '< 1e-10'
    else:
        return f'= {p:.2}'

def print_values(correlation_coefs, correlation_coefs_err, ax, value=True, pvalue_given=False, test=0):
    nx, ny = correlation_coefs.shape
    for k in range(nx):
        for j in range(ny):
            if k >= j:
                label = f'{np.around(correlation_coefs[j, k], 2):.2f}\n' if value else ''

                pvalue = 0
                if pvalue_given:
                    pvalue = correlation_coefs_err[j, k]
                else:
                    pvalue = p_value(correlation_coefs[j, k], test, correlation_coefs_err[j, k])

                if pvalue < 0.001:
                    label += '***'
                elif pvalue < 0.01:
                    label += '**'
                elif pvalue < 0.05:
                    label += '*'
                else:
                    label += 'ns'
                text = ax.text(k, j, label, ha='center', va='center', color='w')

def print_values_all(correlation_coefs, correlation_coefs_err, ax, value=True, pvalue_given=False, test=0):
    nx, ny = correlation_coefs.shape
    for k in range(nx):
        for j in range(ny):
            label = f'{np.around(correlation_coefs[k, j], 2):.2f}\n' if value else ''

            pvalue = 0
            if pvalue_given:
                pvalue = correlation_coefs_err[k, j]
            else:
                pvalue = p_value(correlation_coefs[k, j], test, correlation_coefs_err[k, j])

            if pvalue < 0.001:
                label += '***'
            elif pvalue < 0.01:
                label += '**'
            elif pvalue < 0.05:
                label += '*'
            else:
                label += 'ns'
            text = ax.text(j, k, label, ha='center', va='center', color='w', fontsize='x-small')
