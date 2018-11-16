import libs.extremumlib as elib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_trend(window):
    n = len(window)
    x = np.arange(n)
    print("len(x)", len(x), n, len(window))

    A = [
        [2 * sum(x), 2 * n],
        [2 * sum(x ** 2), 2 * sum(x)]
    ]
    b = [2 * sum(window), 2 * sum(x * window)]
    res = np.linalg.solve(A, b)
    print(res)
    trend = res[0] * x + res[1]
    return trend


def get_bound_by_hist(window, pref_prob = 0.2, suff_prob = 0.2,  wname ='db6', quant_num = 50, mod = (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)):

    # plt.figure()
    # window = np.array(window)
    # plt.plot(window)
    window = np.array(window).astype(float)
    tmp = window.copy()
    # mod = [0 for i in range(10)]

    colors = ['r', 'g', 'y', 'w', 'violet']

    tmp = elib.wavedec_filtration(tmp, mod, wname=wname)
    # window = elib.wavedec_filtration(window, [0, 0], wname ='haar')
    window -= tmp
    # plt.plot(tmp)
    print(window)
    maxy = np.max(window)
    miny = np.min(window)
    print(maxy, miny)
    dt = (maxy - miny)/ quant_num
    y0 = miny
    #
    y_vals = np.linspace(miny, maxy, quant_num + 1)[1:]
    cnt_vals = np.zeros(quant_num)

    for y in window:
        ptr = (y - y0 - 1e-8) // dt
        cnt_vals[int(ptr)] += 1

    cnt_all = len(window)

    cnt_vals /= cnt_all

    # print(sum(cnt_vals))

    # plt.figure()
    # plt.plot(y_vals, cnt_vals)
    # plt.figure()
    # plt.plot(y_vals)

    pref_sum = np.zeros(len(cnt_vals) + 1)
    suff_sum = np.zeros(len(cnt_vals) + 1)

    pref_sum[1:] = cnt_vals.copy()
    suff_sum[:-1] = cnt_vals.copy()

    for i in range(1, len(pref_sum)):
        pref_sum[i] += pref_sum[i - 1]

    for i in range(len(pref_sum) - 2, -1, -1):
        suff_sum[i] += suff_sum[i + 1]

    # plt.figure()
    # plt.plot(y_vals, pref_sum[1:])
    # plt.plot(y_vals, suff_sum[:-1])

    # plt.figure()
    # n, bins, patches = plt.hist(window[:256], 100, density=True, facecolor='g', alpha=0.75)
    # plt.show()

    ptr_pref = 0
    ptr_suff = 0

    for i in range(len(pref_sum[1:])):
        if(pref_sum[i] >= pref_prob):
            ptr_pref = i
            break

    for i in range(len(pref_sum[:-1]) - 1, -1, -1):
        if(suff_sum[i] >= suff_prob):
            ptr_suff = i
            break

    # print(y_vals[ptr_pref], y_vals[ptr_suff])
    return y_vals[ptr_pref], y_vals[ptr_suff], tmp


def get_bound_by_hist_linear_approx(window, pref_prob = 0.2, suff_prob = 0.2,  wname ='db6', quant_num = 50, mod = (1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)):

    # plt.figure()
    # window = np.array(window)
    # plt.plot(window)
    window = np.array(window).astype(float)
    tmp = window.copy()
    # mod = [0 for i in range(10)]

    colors = ['r', 'g', 'y', 'w', 'violet']

    tmp = get_trend(window)
    # window = elib.wavedec_filtration(window, [0, 0], wname ='haar')
    window -= tmp
    # plt.plot(tmp)
    print(window)
    maxy = np.max(window)
    miny = np.min(window)
    print(maxy, miny)
    dt = (maxy - miny)/ quant_num
    y0 = miny
    #
    y_vals = np.linspace(miny, maxy, quant_num + 1)[1:]
    cnt_vals = np.zeros(quant_num)

    for y in window:
        ptr = (y - y0 - 1e-8) // dt
        cnt_vals[int(ptr)] += 1

    cnt_all = len(window)

    cnt_vals /= cnt_all

    # print(sum(cnt_vals))

    # plt.figure()
    # plt.plot(y_vals, cnt_vals)
    # plt.figure()
    # plt.plot(y_vals)

    pref_sum = np.zeros(len(cnt_vals) + 1)
    suff_sum = np.zeros(len(cnt_vals) + 1)

    pref_sum[1:] = cnt_vals.copy()
    suff_sum[:-1] = cnt_vals.copy()

    for i in range(1, len(pref_sum)):
        pref_sum[i] += pref_sum[i - 1]

    for i in range(len(pref_sum) - 2, -1, -1):
        suff_sum[i] += suff_sum[i + 1]

    # plt.figure()
    # plt.plot(y_vals, pref_sum[1:])
    # plt.plot(y_vals, suff_sum[:-1])

    # plt.figure()
    # n, bins, patches = plt.hist(window[:256], 100, density=True, facecolor='g', alpha=0.75)
    # plt.show()

    ptr_pref = 0
    ptr_suff = 0

    for i in range(len(pref_sum[1:])):
        if(pref_sum[i] >= pref_prob):
            ptr_pref = i
            break

    for i in range(len(pref_sum[:-1]) - 1, -1, -1):
        if(suff_sum[i] >= suff_prob):
            ptr_suff = i
            break

    # print(y_vals[ptr_pref], y_vals[ptr_suff])
    return y_vals[ptr_pref], y_vals[ptr_suff], tmp