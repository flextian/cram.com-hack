from PyQt5 import QtCore, QtGui, QtWidgets
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

class Ui_Dialog(object):

    def actualthing(self):
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        gameUrl = self.lineEdit_3.text()
        gameId = 2
        if "jewel" in gameUrl:
            gameId = 1
        score = int(self.lineEdit_4.text())
        accuracy = int(self.lineEdit_5.text())
        time = self.lineEdit_6.text()

        '''getting the session variables'''
        driver = webdriver.Chrome(options=chromeOptions)
        driver.set_window_size(1000,1000)
        driver.get("https://www.cram.com/user/login")
        usernameElement = driver.find_element_by_id("username")
        usernameElement.send_keys(username)
        passwordElement = driver.find_element_by_id("password")
        passwordElement.send_keys(password)
        loginButtonElement = driver.find_element_by_id("loginButton")
        loginButtonElement.click()

        '''Going to the game and getting the variables'''
        driver.get(gameUrl)
        allTheInfo = driver.find_element_by_class_name("body")
        allTheInfo = allTheInfo.find_element_by_tag_name("script")
        allTheInfo = allTheInfo.get_attribute("innerHTML")

        '''Turning all the js variables into python dictionary'''
        allTheInfoDict = {}
        numberOfVariables = allTheInfo.count("var")
        for x in range(numberOfVariables):
            variableName = allTheInfo[allTheInfo.index("var") + 4 : allTheInfo.index("=") - 1]
            variableValue = allTheInfo[allTheInfo.index("=") + 2 : allTheInfo.index(";")]
            if variableValue[0] is '"' or variableValue[0] is "'":
                variableValue = variableValue[1:-1]
            else:
                variableValue = int(variableValue)
            allTheInfoDict.update({variableName : variableValue})
            allTheInfo = allTheInfo[allTheInfo.index(";") + 1:]


        '''Setting the params for the url send'''
        params = {}
        params['userId'] = allTheInfoDict['userId']
        params['setId'] = allTheInfoDict['setId']
        params['score'] = score
        params['time'] = time
        params['limit'] = 10
        params['name'] = allTheInfoDict['userName']
        params['accuracy'] = accuracy
        params['userBestScore'] = allTheInfoDict['userBestScore']
        params['gameId'] = gameId
        #1 or 2 depending on game
        params['hasImages'] = False

        '''The weird formula to calculate the url '''
        def prepareParams(params):
            jsonString = json.dumps(params)
            params2 = ''
            asciiVar = None
            for x in range(len(jsonString)):
                asciiVar = str(((255 - ord(jsonString[x])) + (x % allTheInfoDict["prepareParamsMod"])))
                if len(asciiVar) < 2:
                    asciiVar = '00' + asciiVar
                elif len(asciiVar) < 3:
                    asciiVar = '0' + asciiVar
                params2 += asciiVar
            return "?params=" + params2


        '''Visit the URL to send the data'''
        finalUrl = 'https://www.cram.com/games/save-score' + prepareParams(params)
        driver.get(finalUrl)
        driver.close()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(396, 326)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(90, 20, 191, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 61, 20))
        self.label.setObjectName("<la></la>bel")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 60, 191, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 61, 20))
        self.label_2.setObjectName("label_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(90, 100, 281, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 55, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 180, 55, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(90, 180, 281, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 391, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(10, 150, 381, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(20, 220, 55, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_5 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_5.setGeometry(QtCore.QRect(90, 220, 281, 22))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(20, 260, 55, 16))
        self.label_8.setObjectName("label_8")
        self.lineEdit_6 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(90, 260, 281, 22))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_6.setText("0")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(90, 290, 201, 16))
        self.label_9.setObjectName("label_9")
        '''
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(20, 310, 201, 16))
        self.label_10.setObjectName("label_9")
        self.outputBox = QtWidgets.QPlainTextEdit(Dialog)
        self.outputBox.setGeometry(QtCore.QRect(90, 310, 281, 100))
        self.outputBox.setObjectName("outputBox")
        '''
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.actualthing)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Username"))
        self.label_2.setText(_translate("Dialog", "Password"))
        self.label_3.setText(_translate("Dialog", "Game Url"))
        self.label_4.setText(_translate("Dialog", "Score"))
        self.label_5.setText(_translate("Dialog", "Example: https://www.cram.com/flashcards/games/stellar-speller"))
        self.label_6.setText(_translate("Dialog", "/equine-acupuncture-point-chi-session-2-2266675"))
        self.label_7.setText(_translate("Dialog", "Accuracy"))
        self.label_8.setText(_translate("Dialog", "Time"))
        self.label_9.setText(_translate("Dialog", "Only matters in Jewels of Wisdom"))
        #self.label_10.setText(_translate("Dialog", "Output: "))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())