from keras.models import Model
from keras.layers import Dense, Dropout, LSTM, Input, Activation
import tensorflow as tf
import numpy as np
from predictions.util import csv_to_dataset, history_points
import matplotlib.pyplot as plt

seed_value = 4
np.random.seed(seed_value)
tf.random.set_seed(seed_value)

btc = "./datasets/bitcoin_2010-11-1_2021-12-13.csv"
cro = "./datasets/crypto-com-coin_2018-12-14_2021-12-13.csv"


def predict():
    ohlcv_histories, _, next_day_open_values, unscaled_y, y_normaliser = csv_to_dataset(btc)
    
    test_split = 0.9
    n = int(ohlcv_histories.shape[0] * test_split)
    
    ohlcv_train = ohlcv_histories[:n]
    y_train = next_day_open_values[:n]
    
    ohlcv_test = ohlcv_histories[n:]
    y_test = next_day_open_values[n:]
    
    unscaled_y_test = unscaled_y[n:]
    
    print(ohlcv_train.shape)
    print(ohlcv_test.shape)
    
    # model architecture
    
    lstm_input = Input(shape=(history_points, 5), name='lstm_input')
    x = LSTM(50, name='lstm_0')(lstm_input)
    x = Dropout(0.2, name='lstm_dropout_0')(x)
    x = Dense(64, name='dense_0')(x)
    x = Activation('sigmoid', name='sigmoid_0')(x)
    x = Dense(1, name='dense_1')(x)
    output = Activation('linear', name='linear_output')(x)
    
    model = Model(inputs=lstm_input, outputs=output)
    adam = tf.optimizers.Adam(lr=0.0005)
    model.compile(optimizer=adam, loss='mse')
    model.fit(x=ohlcv_train, y=y_train, batch_size=32, epochs=50, shuffle=True, validation_split=0.1)
    
    # evaluation
    y_test_predicted = model.predict(ohlcv_test)
    y_test_predicted = y_normaliser.inverse_transform(y_test_predicted)
    y_predicted = model.predict(ohlcv_histories)
    y_predicted = y_normaliser.inverse_transform(y_predicted)
    
    assert unscaled_y_test.shape == y_test_predicted.shape
    real_mse = np.mean(np.square(unscaled_y_test - y_test_predicted))
    scaled_mse = real_mse / (np.max(unscaled_y_test) - np.min(unscaled_y_test)) * 100
    print(scaled_mse)
    
    plt.gcf().set_size_inches(22, 15, forward=True)
    
    start = 0
    end = -1
    
    real = plt.plot(unscaled_y_test[start:end], label='real')
    pred = plt.plot(y_test_predicted[start:end], label='predicted')
    
    # real = plt.plot(unscaled_y[start:end], label='real')
    # pred = plt.plot(y_predicted[start:end], label='predicted')
    
    plt.legend(['Real', 'Predicted'])
    plt.show()

    model.save(f'model.h5')


if __name__ == '__main__':
    predict()
    print("done")
