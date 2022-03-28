import pandas as pd


class Trader:

    def setup(self, **params):
        pass

    def consume(self,  data: list):
        pass


class Wallet:

    def __init__(self, init_amount: float):
        self.__amount__ = init_amount

    def get_amount(self):
        return self.__amount__

    def buy(self, amount: float):
        pass

    def sell(self, amount: float):
        pass


class DumpTrader(Trader):

    __buys__: list
    __future_sells__: list
    __sells__: list
    __delta_buy__: float
    __delta_sell__: float
    __data_history__: list
    __wallet__: Wallet

    def __init__(self, d_buy, d_sell, init_amount: float):
        self.__buys__ = []
        self.__future_sells__ = []
        self.__sells__ = []
        self.__delta_buy__ = d_buy
        self.__delta_sell__ = d_sell
        self.__data_history__ = []
        self.__wallet__ = Wallet(init_amount)

    def setup(self, **params):
        pass

    def consume(self, data: list):
        # TODO init buy

        # TODO buy when the price is in a block lower of max_buy
        # sell if it buy in a lower position
        # sell or buy only at the end of each list of data
        pass

    def get_sells(self):
        return self.__sells__


if __name__ == "__main__":

    dump_trader = DumpTrader(d_buy=2.0, d_sell=2.0, init_amount=1000)
    csv_path = "../datasets/crypto-com-coin_2018-12-14_2021-12-13.csv"
    data = pd.read_csv(csv_path, usecols=["date", "open"])

    for d in data:
        dump_trader.consume(d)

    # TODO analyze statistics
