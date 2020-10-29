from PyQt5 import QtWidgets, QtGui
from ui.mainUi import Ui_MainWindow as UIM
from kiwoom.kiwoom import Kiwoom
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import mpl_finance
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

        self.fig, self.axs = plt.subplots(2,1, sharex=True)
        self.canvas = FigureCanvas(self.fig)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.toolbar)

        # self.ax.label_outer()
        # self.bx.label_outer()

    #정의
    def allEvent(self): #종목코드가 변경되었을 때 모든 데이터 및, Ui 재설정
        self.kiwoom.set_jongCode(self.stockCBB.currentText())

        data = self.kiwoom.get_dayChartSearchDataframe()

        print(data)



        print('2')
        self.axs[0].xaxis.set_major_formatter(ticker.FixedFormatter(data['일자'].tolist()))

        num = data['일자'].tolist()


        def x_date(x,pos):
            try:
                return num[int(x-0.5)]
            except IndexError:
                return ''
        self.axs[0].clear()
        self.axs[1].clear()
        self.axs[0].set_ylim([0,50000])
        self.axs[0].xaxis.set_major_locator(ticker.MaxNLocator(10))
        self.axs[1].xaxis.set_major_formatter(ticker.FuncFormatter(x_date))

        mpl_finance.candlestick2_ochl(self.axs[0], data['시가'], data['고가'], data['저가'], data['현재가'], width=0.5, colorup='r', colordown='b')

        colors = []
        j = 0
        for i in data['거래량'].tolist():
            if i > 100000:
                if j %3 == 0:
                    colors.append("black")
                else:
                    colors.append('red')
                j = j+1
            else:
                colors.append("red")

        self.axs[1].bar(data.index, data['거래량'],  label='b', color=colors)
        self.axs[0].grid()
        self.axs[1].grid()
        print('3')

        self.canvas.draw()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainEvent()
    ui.show()
    sys.exit(app.exec_())




