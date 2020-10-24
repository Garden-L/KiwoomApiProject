from PyQt5 import QtWidgets
from ui.mainUi import Ui_MainWindow as UIM
from kiwoom.kiwoom import Kiwoom
import datetime
import plotly
import pandas as pd
import matplotlib.pyplot as plt
import time

class Ui_MainEvent(UIM, QtWidgets.QMainWindow):
    def __init__(self):
    #--------Kiwoom----------#
        self.kiwoom = Kiwoom()

        #kiwwom login
        self.kiwoom.signal_login_commCorrect()

        #종목코드 가져오기
        self.kiwoom.get_jongmokCode()

        super().__init__()
        self.setupUI()


    def setupUI(self): #Make widgets
        '''
        :param MainWindow: Mainwindow widget
        :return:
        '''
        super().setupUi(self)
        print(self)

        self.stockCBB.addItems(self.kiwoom.jongmokCode)

    #정의
    def allEvent(self): #종목코드가 변경되었을 때 모든 데이터 및, Ui 재설정
        self.kiwoom.set_jongCode(self.stockCBB.currentText())

        data = self.kiwoom.get_dayChartSearchDataframe()

        print(data,'wlflwi')
        # fig = plotly.graph_objs.Figure(plotly.graph_objs.Candlestick(x = data['일자'], open=data['시가'], high=data['고가'], low=data['저가'], close=data['종가']))
        # fig.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainEvent()
    ui.show()
    sys.exit(app.exec_())




