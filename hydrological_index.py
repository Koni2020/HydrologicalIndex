import numpy as np
from numba import njit
import pandas as pd
import baseflow
# @njit
def vect2array(vect_):
    vect_ = vect_.reshape(vect_.size)
    array = []
    i = 0
    while True:
        if i >= vect_.size - 2:
            break
        vect = []
        while (~np.isnan(vect_[i + 1])) & (~np.isnan(vect_[i])):
            vect.append(vect_[i])
            if i >= vect_.size - 2:
                i = vect_.size
                break
            i += 1
        else:
            if len(vect) >= 1:
                array.append(vect)
        i += 1

    m = len(array)
    if m == 0:
        return np.nan
    n = np.max([len(x) for x in array])
    container = np.full([m, n], np.nan)
    n = 0
    for i in array:
        container[n, 0:len(i)] = i
        n += 1
    return container


def calculate_average_duration(vect):
    if np.isnan(vect.values).all():
        return np.nan
    else:
        consecutive_array = vect2array(vect.values)
        if isinstance(consecutive_array, float):
            return np.nan
        else:
            consecutive_array[~np.isnan(consecutive_array)] = 1
            return np.mean(consecutive_array.sum(axis=1).mean())

def calculate_half_streamflow_time(vect):
    tf = vect.sum()
    vect = vect.cumsum()
    vect = np.abs(vect - tf / 2)
    idx = np.argmin(vect)
    return idx + 1

def calclulate_RB_index(vect):
    ts = vect.sum()
    return vect.diff().abs().sum() / ts

def main_compute(sf):
    bf = baseflow.Eckhardt(sf.values, a=0.925, BFImax=0.8, b_LH=sf.values[0])
    bf = pd.DataFrame(index=sf.index, data=bf, columns=sf.columns)
    # Magnitude
    Qmax1 = sf.rolling(window=1).mean().groupby(sf.index.year).max()
    Qmax3 = sf.rolling(window=3).mean().groupby(sf.index.year).max()
    Qmax7 = sf.rolling(window=7).mean().groupby(sf.index.year).max()
    Qmax30 = sf.rolling(window=30).mean().groupby(sf.index.year).max()
    Qmax90 = sf.rolling(window=90).mean().groupby(sf.index.year).max()

    Qmax1p = sf.rolling(window=1).mean().groupby(sf.index.year).max() / sf.groupby(sf.index.year).sum() * 100
    Qmax3p = sf.rolling(window=3).mean().groupby(sf.index.year).max() / sf.groupby(sf.index.year).sum() * 100
    Qmax7p = sf.rolling(window=7).mean().groupby(sf.index.year).max() / sf.groupby(sf.index.year).sum() * 100
    Qmax30p = sf.rolling(window=30).mean().groupby(sf.index.year).max() / sf.groupby(sf.index.year).sum() * 100

    Qmin1 = sf.rolling(window=1).mean().groupby(sf.index.year).min()
    Qmin3 = sf.rolling(window=3).mean().groupby(sf.index.year).min()
    Qmin7 = sf.rolling(window=7).mean().groupby(sf.index.year).min()
    Qmin30 = sf.rolling(window=30).mean().groupby(sf.index.year).min()
    Qmin90 = sf.rolling(window=90).mean().groupby(sf.index.year).min()

    Q1st = sf.groupby(sf.index.year).apply(np.quantile, q=0.01)
    Q5th = sf.groupby(sf.index.year).apply(np.quantile, q=0.05)
    Q10th = sf.groupby(sf.index.year).apply(np.quantile, q=0.10)
    Q25th = sf.groupby(sf.index.year).apply(np.quantile, q=0.25)
    Q50th = sf.groupby(sf.index.year).apply(np.quantile, q=0.50)
    Q75th = sf.groupby(sf.index.year).apply(np.quantile, q=0.75)
    Q90th = sf.groupby(sf.index.year).apply(np.quantile, q=0.90)
    Q95th = sf.groupby(sf.index.year).apply(np.quantile, q=0.95)
    Q99th = sf.groupby(sf.index.year).apply(np.quantile, q=0.99)

    Qmean1 = sf.loc[sf.index.month == 1, :].resample('Y').mean()
    Qmean1.index = Qmean1.index.year

    Qmean2 = sf.loc[sf.index.month == 2, :].resample('Y').mean()
    Qmean2.index = Qmean2.index.year

    Qmean3 = sf.loc[sf.index.month == 3, :].resample('Y').mean()
    Qmean3.index = Qmean3.index.year

    Qmean4 = sf.loc[sf.index.month == 4, :].resample('Y').mean()
    Qmean4.index = Qmean4.index.year

    Qmean5 = sf.loc[sf.index.month == 5, :].resample('Y').mean()
    Qmean5.index = Qmean5.index.year

    Qmean6 = sf.loc[sf.index.month == 6, :].resample('Y').mean()
    Qmean6.index = Qmean6.index.year

    Qmean7 = sf.loc[sf.index.month == 7, :].resample('Y').mean()
    Qmean7.index = Qmean7.index.year

    Qmean8 = sf.loc[sf.index.month == 8, :].resample('Y').mean()
    Qmean8.index = Qmean8.index.year

    Qmean9 = sf.loc[sf.index.month == 9, :].resample('Y').mean()
    Qmean9.index = Qmean9.index.year

    Qmean10 = sf.loc[sf.index.month == 10, :].resample('Y').mean()
    Qmean10.index = Qmean10.index.year

    Qmean11 = sf.loc[sf.index.month == 11, :].resample('Y').mean()
    Qmean11.index = Qmean11.index.year

    Qmean12 = sf.loc[sf.index.month == 12, :].resample('Y').mean()
    Qmean12.index = Qmean12.index.year

    RM = sf.groupby(sf.index.year).max() - sf.groupby(sf.index.year).min()
    BM = bf.groupby(bf.index.year).max() - bf.groupby(bf.index.year).min()

    Qhigh = 9 * np.percentile(sf, 50)
    Qlow = 0.2 * sf.values.mean()

    FreH = sf[sf > Qhigh].groupby(sf.index.year).count() / 365
    FreL = sf[sf < Qlow].groupby(sf.index.year).count() / 365
    FreZ = sf[sf == 0].groupby(sf.index.year).count() / 365

    Fre1st = sf[sf < np.quantile(sf, 0.01)].groupby(sf.index.year).count() / 365
    Fre5th = sf[sf < np.quantile(sf, 0.5)].groupby(sf.index.year).count() / 365
    Fre95th = sf[sf > np.quantile(sf, 0.95)].groupby(sf.index.year).count() / 365
    Fre99th = sf[sf > np.quantile(sf, 0.99)].groupby(sf.index.year).count() / 365

    NumH = sf[sf > Qhigh].groupby(sf.index.year).count()
    NumL = sf[sf < Qlow].groupby(sf.index.year).count()
    NumZ = sf[sf == 0].groupby(sf.index.year).count()

    Num1st = sf[sf < np.quantile(sf, 0.01)].groupby(sf.index.year).count()
    Num5th = sf[sf < np.quantile(sf, 0.05)].groupby(sf.index.year).count()
    Num95th = sf[sf > np.quantile(sf, 0.95)].groupby(sf.index.year).count()
    Num99th = sf[sf > np.quantile(sf, 0.99)].groupby(sf.index.year).count()

    DurH = sf[sf >= Qhigh].groupby(sf.index.year).apply(calculate_average_duration)
    DurZ = sf[sf == 0].groupby(sf.index.year).apply(calculate_average_duration)
    DurL = sf[sf <= Qlow].groupby(sf.index.year).apply(calculate_average_duration)
    Durl1st = sf[sf <= np.quantile(sf, 0.01)].groupby(sf.index.year).apply(calculate_average_duration)
    Dur5th = sf[sf <= np.quantile(sf, 0.05)].groupby(sf.index.year).apply(calculate_average_duration)
    Dur95th = sf[sf >= np.quantile(sf, 0.95)].groupby(sf.index.year).apply(calculate_average_duration)
    Dur99th = sf[sf >= np.quantile(sf, 0.99)].groupby(sf.index.year).apply(calculate_average_duration)
    RBFI = sf.groupby(sf.index.year).apply(calclulate_RB_index)

    RRmean = sf.diff()[sf.diff() > 0].groupby(sf.index.year).mean()
    RRmedian = sf.diff()[sf.diff() > 0].groupby(sf.index.year).median()
    FRmean = sf.diff()[sf.diff() < 0].groupby(sf.index.year).mean()
    FRmedian = sf.diff()[sf.diff() < 0].groupby(sf.index.year).median()

    HFD = sf.groupby(sf.index.year).apply(calculate_half_streamflow_time)
    MMD = sf.groupby(sf.index.year).idxmax()
    MC7DF = sf.rolling(7).mean().groupby(sf.index.year).idxmin()

    VY = sf.groupby(sf.index.year).var()
    COVY = sf.groupby(sf.index.year).std() / sf.groupby(sf.index.year).mean()
    QCV = (Q75th - Q25th) / Q50th

    RMM = Q50th.to_frame().values / Qmax1
    Q1st = Q1st.to_frame()
    Q5th = Q5th.to_frame()
    Q10th = Q10th.to_frame()
    Q25th = Q25th.to_frame()
    Q50th = Q50th.to_frame()
    Q75th = Q75th.to_frame()
    Q90th = Q90th.to_frame()
    Q95th = Q95th.to_frame()
    Q99th = Q99th.to_frame()
    Qmean = sf.groupby(sf.index.year).mean()
    Qhigh = 9 * Q50th
    Qlow = 0.2 * Qmean
    QCV = QCV.to_frame()
    BM = BM
    BFI = bf.groupby(bf.index.year).mean() / sf.groupby(sf.index.year).mean()
    df = pd.concat([
        Qmax1,
        Qmax3,
        Qmax7,
        Qmax30,
        Qmax90,
        Qmax1p,
        Qmax3p,
        Qmax7p,
        Qmax30p,
        Qmin1,
        Qmin3,
        Qmin7,
        Qmin90,
        Qmin30,
        Q1st,
        Q5th,
        Q10th,
        Q25th,
        Q50th,
        Q75th,
        Q90th,
        Q95th,
        Q99th,
        Qmean1,
        Qmean2,
        Qmean3,
        Qmean4,
        Qmean5,
        Qmean6,
        Qmean7,
        Qmean8,
        Qmean9,
        Qmean10,
        Qmean11,
        Qmean12,
        RM,
        BM,
        FreH,
        FreL,
        FreZ,
        Fre1st,
        Fre5th,
        Fre95th,
        Fre99th,
        NumH,
        NumL,
        NumZ,
        Num1st,
        Num5th,
        Num95th,
        Num99th,
        DurH,
        DurZ,
        DurL,
        Durl1st,
        Dur5th,
        Dur95th,
        Dur99th,
        RBFI,
        RRmean,
        RRmedian,
        FRmean,
        FRmedian,
        HFD,
        MMD,
        MC7DF,
        VY,
        COVY,
        QCV,
        RMM,
        BFI,
        Qmean,
        Qhigh,
        Qlow
    ], axis=1)

    idx_name = \
        '''Qmax1,
        Qmax3,
        Qmax7,
        Qmax30,
        Qmax90,
        Qmax1p,
        Qmax3p,
        Qmax7p,
        Qmax30p,
        Qmin1,
        Qmin3,
        Qmin7,
        Qmin30,
        Qmin90,
        Q1st,
        Q5th,
        Q10th,
        Q25th,
        Q50th,
        Q75th,
        Q90th,
        Q95th,
        Q99th,
        Qmean1,
        Qmean2,
        Qmean3,
        Qmean4,
        Qmean5,
        Qmean6,
        Qmean7,
        Qmean8,
        Qmean9,
        Qmean10,
        Qmean11,
        Qmean12,
        RM,
        BM,
        FreH,
        FreL,
        FreZ,
        Fre1st,
        Fre5th,
        Fre95th,
        Fre99th,
        NumH,
        NumL,
        NumZ,
        Num1st,
        Num5th,
        Num95th,
        Num99th,
        DurH,
        DurZ,
        DurL,
        Durl1st,
        Dur5th,
        Dur95th,
        Dur99th,
        RBFI,
        RRmean,
        RRmedian,
        FRmean,
        FRmedian,
        HFD,
        MMD,
        MC7DF,
        VY,
        COVY,
        QCV,
        RMM,
        BFI,
        Qmean,
        Qhigh,
        Qlow'''
    df.columns = pd.Index(idx_name.split(','))
    return df