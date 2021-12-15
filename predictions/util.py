import pandas as pd
from sklearn import preprocessing
import numpy as np
from sklearn.model_selection import train_test_split

history_points = 50


def csv_to_dataset(csv_path):
    data = pd.read_csv(csv_path, usecols=["open", "high", "low", "close", "volume"])
    data = data.iloc[::-1]
    data = data.values
    
    normalizer = preprocessing.MinMaxScaler()
    dataset = normalizer.fit_transform(data)

    # for each row, generate a dataset with history_points number of elements
    # With data: {open close high low volume} data points, to predict the next open value
    x_ohlcv_norm = np.array(
        [dataset[i:i + history_points].copy() for i in range(len(dataset) - history_points)]
    )
    
    # building the y with the data we want to predict, based on y (the next day open value)
    y_o_norm = np.array(
        [dataset[:, 0][i + history_points].copy() for i in range(len(dataset) - history_points)]
    )
    y_o_norm = np.expand_dims(y_o_norm, axis=-1)
    
    # Add un-normalized data for plotting generation later
    next_day_open_values = np.array([data[:, 0][i + history_points].copy() for i in range(len(data) - history_points)])
    next_day_open_values = np.expand_dims(next_day_open_values, axis=-1)

    y_normaliser = preprocessing.MinMaxScaler()
    y_normaliser.fit(next_day_open_values)

    def calc_ema(values, time_period):
        sma = np.mean(values[:, 3])
        ema_values = [sma]
        k = 2 / (1 + time_period)
        for i in range(len(his) - time_period, len(his)):
            close = his[i][3]
            ema_values.append(close * k + ema_values[-1] * (1 - k))
        return ema_values[-1]

    technical_indicators = []
    for his in x_ohlcv_norm:
        # note since we are using his[3] we are taking the SMA of the closing price
        sma = np.mean(his[:, 3])
        macd = calc_ema(his, 12) - calc_ema(his, 26)
        technical_indicators.append(np.array([sma]))
        # technical_indicators.append(np.array([sma, macd,]))

    technical_indicators = np.array(technical_indicators)

    tech_ind_scaler = preprocessing.MinMaxScaler()
    technical_indicators_normalised = tech_ind_scaler.fit_transform(technical_indicators)

    assert x_ohlcv_norm.shape[0] == y_o_norm.shape[0] == technical_indicators_normalised.shape[0]
    return (
        x_ohlcv_norm,
        technical_indicators_normalised,
        y_o_norm,
        next_day_open_values,
        y_normaliser
    )


def multiple_csv_to_dataset(test_set_name):
    import os
    ohlcv_histories = 0
    technical_indicators = 0
    next_day_open_values = 0
    for csv_file_path in list(filter(lambda x: x.endswith('daily.csv'), os.listdir('./'))):
        if not csv_file_path == test_set_name:
            print(csv_file_path)
            if type(ohlcv_histories) == int:
                ohlcv_histories, technical_indicators, next_day_open_values, _, _ = csv_to_dataset(csv_file_path)
            else:
                a, b, c, _, _ = csv_to_dataset(csv_file_path)
                ohlcv_histories = np.concatenate((ohlcv_histories, a), 0)
                technical_indicators = np.concatenate((technical_indicators, b), 0)
                next_day_open_values = np.concatenate((next_day_open_values, c), 0)

    ohlcv_train = ohlcv_histories
    tech_ind_train = technical_indicators
    y_train = next_day_open_values

    ohlcv_test, tech_ind_test, y_test, unscaled_y_test, y_normaliser = csv_to_dataset(test_set_name)

    return ohlcv_train, tech_ind_train, y_train, ohlcv_test, tech_ind_test, y_test, unscaled_y_test, y_normaliser
