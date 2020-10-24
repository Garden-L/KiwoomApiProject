#응용프로그램 제어 PyQt5에서 제공
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from config.errorCode import *
from pd.pd import *
import datetime
import time

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self.jukaData = Dataset()
        self.input_data = []

        ########################
        self.login_event_loop = None
        ########################
        self.get_ocx_instance()
        self.event_slots()
        #self.signal_login_commCorrect()

        self.get_jongmokCode()

        #self.get_jongmokName() 구현 미흡

    #종목코드 가져오기
    def get_jongmokCode(self):
        self.jongmokCode = self.dynamicCall("GetCodeListByMarket(String)", '0').split(';')


    def get_jongmokName(self):
        pass
        # self.jongmokName = []
        # for i in range(len(self.jongmokCode)):
        #     self.jongmokName.append(self.dynamicCall('GetMasterCodeName(String)', str(self.jongmokCode[i])))

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def event_slots(self):
        print("event")
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)

    def login_slot(self, errCode):
        print(errors(errCode))
        self.login_event_loop.exit()


    def signal_login_commCorrect(self):
        self.dynamicCall("CommConnect()")

        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(String)", "ACCNO")

        self.account_num = account_list.split(';')[0]
        print(f'나의 보유 계좌번호{self.account_num}')

    def detail_account_info(self):
        print('예수금을 요청하는 부분')
        self.dynamicCall("SetInputValue(String, String)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(String, String)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(String, String)", "계좌번호입력매체구문", "00")
        self.dynamicCall("SetInputValue(String, String)", "조회구분", "2")
        self.dynamicCall("CommRqData(String, String, int, String)", "예수금상세현황요청", "opw00001", "0", "2000")

    # 종목코드 설정
    def set_jongCode(self, jongCode):
        self.jongCode = jongCode

    def get_today(self):
        date = datetime.date.today()
        return str(date).replace('-', '')

    def get_dayChartSearchDataframe(self, date = None):
        self.input_data.clear()
        self.get_dayChartSearch(date)

        self.eventloop = QEventLoop()
        self.eventloop.exec_()

        self.jukaData.load(self.input_data)
        self.jukaData.makeDF(None, ['일자', '시가', '고가', '저가', '현재가', '거래량', '거래대금'])

        return self.jukaData.df


    def get_dayChartSearch(self, date = None): #거래량 가져오기
        print("거래량")
        if date == None:
            date = self.get_today()

        self.dynamicCall("SetInputValue(String, String)","종목코드", self.jongCode)
        self.dynamicCall("SetInputValue(String, String)","기준일자", date)
        self.dynamicCall("SetInputValue(String, String)","수정주가구분", "0")
        self.dynamicCall("CommRqData(String, String, String, String)", "주식일봉차트조회요청", "opt10081","0", "1000" )

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        '''
        tr 요청을 받는 구역이다! 슬롯이다!
        :param sScrNo: 스크린번호
        :param sRQName: 내가 요청했을 때 지은 이름
        :param sTrCode: 요청 id, tr코드
        :param sRecordName: 사용안함
        :param sPrevNext:  다음 페이지가 있는지
        :return:
        '''


        print("trdata_slot")
        if sRQName == "예수금상세현황요청":
            deposit = self.dynamicCall("GetCommData(String, String, int, String)",sTrCode, sRQName, 0, "예수금")
            print(f'예수금 {int(deposit)}')

            ok_deposit = self.dynamicCall("GetCommData(String, String, int, String)",sTrCode, sRQName, 0, "출금가능금액")

            print(ok_deposit)

        if sTrCode == "opt10081":
            print('거래량1')
            if sRQName == "주식일봉차트조회요청":
                count = int(self.dynamicCall("GetRepeatCnt(String, String)", sTrCode, sRecordName))
                if count != 0:
                    for index in range(count):
                        m_date = self.dynamicCall("GetCommData(string,QString, int, String)",sTrCode, sRQName,
                                                         index, "일자").strip(" ")
                        openPrice = int(
                            self.dynamicCall("GetCommData(string, String, int, String)",sTrCode, sRQName,
                                                    index, "시가"))
                        highPrice = int(
                            self.dynamicCall("GetCommData(String, String, int, String)",sTrCode, sRQName,
                                                    index, "고가"))
                        lowPrice = int(
                            self.dynamicCall("GetCommData(String, String, int, String)",sTrCode, sRQName,
                                                    index, "저가"))
                        currentPrice = int(
                            self.dynamicCall("GetCommData(String, String, int, String)",sTrCode, sRQName,
                                                    index, "현재가"))
                        volumn = int(
                            self.dynamicCall("GetCommData(String, String, int, String)",sTrCode, sRQName,
                                                    index, "거래량"))
                        tradingValue = int(
                            self.dynamicCall("GetCommData(String, String, int, String)",sTrCode, sRQName,
                                                    index, "거래대금"))

                        self.input_data.append(
                            (m_date, openPrice, highPrice, lowPrice, currentPrice, volumn, tradingValue))

                    if sPrevNext == '2':
                        self.get_dayChartSearch(self.input_data[-1][0])

                    else:
                       self.eventloop.exit()







if __name__ == "__main__":
    krxa = Kiwoom()
    krxa.get_georaeryang('20200101', '005930')
