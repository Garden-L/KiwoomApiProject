from PyQt5 import QtWidgets, QtGui
from ui.mainUi import Ui_MainWindow as UIM
from kiwoom.kiwoom import Kiwoom
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import mpl_finance
import plotly
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

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.toolbar)

        self.ax = self.fig.add_subplot(211)
        self.bx = self.fig.add_subplot(212, sharex = self.ax)
        # self.ax.label_outer()
        # self.bx.label_outer()

    #정의
    def allEvent(self): #종목코드가 변경되었을 때 모든 데이터 및, Ui 재설정
        self.kiwoom.set_jongCode(self.stockCBB.currentText())

        data = self.kiwoom.get_dayChartSearchDataframe()

        print(data)



        print('2')
        self.ax.xaxis.set_major_formatter(ticker.FixedFormatter(data['일자'].tolist()))
        num = []
        for i in range(len(data['일자'].tolist())):
            num.append(i)
        self.ax.xaxis.set_major_locator(ticker.FixedLocator(num))

        mpl_finance.candlestick2_ochl(self.ax, data['시가'], data['고가'], data['저가'], data['현재가'], width=0.5, colorup='r', colordown='b')

        self.bx.plot(data.index, data['거래량'], label='b')
        self.ax.grid()
        self.bx.grid()
        print('3')

        self.canvas.draw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainEvent()
    ui.show()
    sys.exit(app.exec_())




