from keras.models import Model
from keras.layers import Dense, Dropout, LSTM, Input, Activation, concatenate
import tensorflow as tf
import numpy as np
from predictions.util import csv_to_dataset, history_points
from sklearn.model_selection import TimeSeriesSplit, train_test_split

from keras.models import load_model

seed_value = 4
np.random.seed(seed_value)
tf.random.set_seed(seed_value)

btc = "./datasets/bitcoin_2010-11-1_2021-12-13.csv"
cro = "./datasets/crypto-com-coin_2018-12-14_2021-12-13.csv"


def train(X_train, y_train, tech_ind_train, technical_indicators):
    # model architecture
    
    # define two sets of inputs
    lstm_input = Input(shape=(history_points, 5), name='lstm_input')
    dense_input = Input(shape=(technical_indicators.shape[1],), name='tech_input')
    
    # the first branch operates on the first input
    x = LSTM(50, name='lstm_0')(lstm_input)
    x = Dropout(0.2, name='lstm_dropout_0')(x)
    lstm_branch = Model(inputs=lstm_input, outputs=x)
    
    # the second branch opreates on the second input
    y = Dense(20, name='tech_dense_0')(dense_input)
    y = Activation("relu", name='tech_relu_0')(y)
    y = Dropout(0.2, name='tech_dropout_0')(y)
    technical_indicators_branch = Model(inputs=dense_input, outputs=y)
    
    # combine the output of the two branches
    combined = concatenate([lstm_branch.output, technical_indicators_branch.output], name='concatenate')
    
    z = Dense(64, activation="sigmoid", name='dense_pooling')(combined)
    z = Dense(1, activation="linear", name='dense_out')(z)
    
    # our model will accept the inputs of the two branches and
    # then output a single value
    model = Model(inputs=[lstm_branch.input, technical_indicators_branch.input], outputs=z)
    adam = tf.optimizers.Adam(learning_rate=0.0005)
    model.compile(optimizer=adam, loss='mse')
    model.fit(x=[X_train, tech_ind_train], y=y_train, batch_size=32, epochs=20, shuffle=True, validation_split=0.1)

    model.save(f'model.h5')


def predict():
    X, technical_indicators, y, unscaled_y, y_normaliser = csv_to_dataset(cro)
    
    test_size = 100
    
    X_train, X_test, y_train, y_test = None, None, None, None

    for train_index, test_index in TimeSeriesSplit(n_splits=2, test_size=test_size).split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

    tech_ind_train = technical_indicators[test_size:]
    tech_ind_test = technical_indicators[:test_size]
    unscaled_y_test = unscaled_y[:test_size]

    print(X_train.shape)
    print(X_test.shape)
    
    # train
    train(X_train, y_train, tech_ind_train, technical_indicators)

    # Predictions
    model = load_model('model.h5')
    
    y_test_predicted = model.predict([X_test, tech_ind_test])
    y_test_predicted = y_normaliser.inverse_transform(y_test_predicted)
    y_predicted = model.predict([X, technical_indicators])
    y_predicted = y_normaliser.inverse_transform(y_predicted)
    assert unscaled_y_test.shape == y_test_predicted.shape
    real_mse = np.mean(np.square(unscaled_y_test - y_test_predicted))
    scaled_mse = real_mse / (np.max(unscaled_y_test) - np.min(unscaled_y_test)) * 100
    print(scaled_mse)

    import matplotlib.pyplot as plt

    plt.gcf().set_size_inches(22, 15, forward=True)

    start = 0
    end = -1

    real = plt.plot(unscaled_y_test[start:end], label='real')
    pred = plt.plot(y_test_predicted[start:end], label='predicted')
    pred2 = plt.plot(y_test_predicted[start:50], label='future')

    # real = plt.plot(unscaled_y[start:end], label='real')
    # pred = plt.plot(y_predicted[start:end], label='predicted')

    plt.legend(['Real', 'Predicted'])

    plt.show()


if __name__ == '__main__':
    predict()
    print("done")
