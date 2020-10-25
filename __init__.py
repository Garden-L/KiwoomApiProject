from PyQt5 import QtWidgets, QtGui
from ui.mainUi import Ui_MainWindow as UIM
from kiwoom.kiwoom import Kiwoom
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
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

    #정의
    def allEvent(self): #종목코드가 변경되었을 때 모든 데이터 및, Ui 재설정
        self.kiwoom.set_jongCode(self.stockCBB.currentText())

        data = self.kiwoom.get_dayChartSearchDataframe()

        print(data)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar =NavigationToolbar(self.canvas, self)

        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.toolbar)
        print("1")

        ax = self.fig.add_subplot(211)
        print('2')
        ax.plot(data.index, data['고가'],label = 'a')
        ax = self.fig.add_subplot(212)
        ax.plot(data.index, data['거래량'],label ='b')
        ax.grid()
        print('3')

        self.canvas.draw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainEvent()
    ui.show()
    sys.exit(app.exec_())




