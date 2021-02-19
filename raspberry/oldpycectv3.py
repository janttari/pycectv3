#!/usr/bin/env python3
#
#TODO: alapalkki katoaa AINA alaspainikkeella. kanavalistan <-- ei toimi
ALAMENUKORKEUS=60
KANAVALISTALEVEYS=600
NAPIT = {1: "YLÖS", 0: "OK", 2: "ALAS", 3: "VASEN", 4: "OIKEA", 69: "STOP", 70: "PAUSE", 72: "REV", 73: "FWD", 68: "PLAY"}

import cec
import requests
import ctypes
import time
import vlc
import json
import urllib.parse
#from PyQt5 import QtNetwork !TODO siirrä requestit
from configobj import ConfigObj
import os.path
from pathlib import Path


home = str(Path.home())
print(home)
if not os.path.exists(home+"/.config/pycectv.conf"):
    print("konfiguraatiotiedosto ~/.config/pycectv.conf puuttuu!")
    quit()
config=ConfigObj(home+"/.config/pycectv.conf")
ENIGMAURL=config.get("enigmaurl")
if len(ENIGMAURL)<5:
    print("enigmaurl puuttuu asetustiedostosta")
    quit()
kayttaja=config.get("user")
salasana=config.get("pass")

if salasana is not None:
    alku,loppu=ENIGMAURL.split("://") 
    ENIGMAURL=alku+"://"+kayttaja+":"+salasana+"@"+loppu


#################################################
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(QtCore.QObject):
    signal = QtCore.pyqtSignal([str])

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1014, 853)
        Form.setStyleSheet("")
        self.frame_kanavalista = QtWidgets.QFrame(Form)
        self.frame_kanavalista.setGeometry(QtCore.QRect(0, 0, 211, 441))
        self.frame_kanavalista.setStyleSheet("background-color: rgba(0, 0,255);")
        self.frame_kanavalista.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_kanavalista.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_kanavalista.setObjectName("frame_kanavalista")
        self.list_kohteet = QtWidgets.QListWidget(self.frame_kanavalista)
        self.list_kohteet.setGeometry(QtCore.QRect(10, 60, 191, 351))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.list_kohteet.setFont(font)
        self.list_kohteet.setStyleSheet("QListView{\n"
"background-color:rgb(41, 85, 74,50); \n"
"font: 24pt \"Ubuntu\";\n"
"color: white;}\n"
"\n"
"QListView::item:selected{\n"
"background-color: rgb(75,153,134); \n"
"color: yellow;};\n"
"\n"
"")
        self.list_kohteet.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_kohteet.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_kohteet.setIconSize(QtCore.QSize(0, 0))
        self.list_kohteet.setObjectName("list_kohteet")
        self.frame_soitin = QtWidgets.QFrame(Form)
        self.frame_soitin.setGeometry(QtCore.QRect(70, 0, 741, 611))
        self.frame_soitin.setStyleSheet("background-color: rgb(99, 255, 99);\n"
"border:none;")
        self.frame_soitin.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_soitin.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_soitin.setObjectName("frame_soitin")
        self.frame_raidat = QtWidgets.QFrame(Form)
        self.frame_raidat.setGeometry(QtCore.QRect(700, 310, 281, 241))
        self.frame_raidat.setStyleSheet("background-color: rgba(0, 0,255, 50);")
        self.frame_raidat.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_raidat.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_raidat.setObjectName("frame_raidat")
        self.list_sraidat = QtWidgets.QListWidget(self.frame_raidat)
        self.list_sraidat.setGeometry(QtCore.QRect(60, 120, 171, 111))
        self.list_sraidat.setStyleSheet("QListView{\n"
"background-color:rgb(41, 85, 74,50); \n"
"font: 24pt \"Ubuntu\";\n"
"color: white;}\n"
"\n"
"QListView::item:selected{\n"
"background-color: rgb(75,153,134,50); \n"
"color: yellow;};\n"
"\n"
"")
        self.list_sraidat.setObjectName("list_sraidat")
        self.list_araidat = QtWidgets.QListWidget(self.frame_raidat)
        self.list_araidat.setGeometry(QtCore.QRect(70, 10, 151, 91))
        self.list_araidat.setStyleSheet("QListView{\n"
"background-color:rgb(41, 85, 74,50); \n"
"font: 24pt \"Ubuntu\";\n"
"color: white;}\n"
"\n"
"QListView::item:selected{\n"
"background-color: rgb(75,153,134,50); \n"
"color: yellow;};\n"
"\n"
"")
        self.list_araidat.setObjectName("list_araidat")
        self.frame_info = QtWidgets.QFrame(Form)
        self.frame_info.setGeometry(QtCore.QRect(740, 80, 241, 151))
        self.frame_info.setStyleSheet("background-color: rgb(54, 54, 54,100);")
        self.frame_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_info.setObjectName("frame_info")
        self.label_info = QtWidgets.QLabel(self.frame_info)
        self.label_info.setGeometry(QtCore.QRect(80, 30, 131, 81))
        self.label_info.setStyleSheet("background-color: rgb(255, 216, 123);")
        self.label_info.setObjectName("label_info")
        self.frame_alamenu = QtWidgets.QFrame(Form)
        self.frame_alamenu.setGeometry(QtCore.QRect(90, 590, 691, 80))
        self.frame_alamenu.setStyleSheet("background-color: rgba(255, 0, 0, 50);")
        self.frame_alamenu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_alamenu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_alamenu.setObjectName("frame_alamenu")
        self.btn_tv = QtWidgets.QToolButton(self.frame_alamenu)
        self.btn_tv.setGeometry(QtCore.QRect(200, 0, 34, 60))
        self.btn_tv.setObjectName("btn_tv")
        self.btn_movie = QtWidgets.QToolButton(self.frame_alamenu)
        self.btn_movie.setGeometry(QtCore.QRect(250, 0, 51, 60))
        self.btn_movie.setObjectName("btn_movie")
        self.btn_subtitle = QtWidgets.QToolButton(self.frame_alamenu)
        self.btn_subtitle.setGeometry(QtCore.QRect(320, 0, 81, 60))
        self.btn_subtitle.setObjectName("btn_subtitle")
        self.btn_audio = QtWidgets.QToolButton(self.frame_alamenu)
        self.btn_audio.setGeometry(QtCore.QRect(420, 0, 61, 60))
        self.btn_audio.setObjectName("btn_audio")
        self.btnsulje = QtWidgets.QToolButton(self.frame_alamenu)
        self.btnsulje.setGeometry(QtCore.QRect(520, 0, 97, 60))
        self.btnsulje.setObjectName("btnsulje")
        self.btn_tmpalamenu = QtWidgets.QPushButton(Form)
        self.btn_tmpalamenu.setGeometry(QtCore.QRect(800, 10, 97, 33))
        self.btn_tmpalamenu.setStyleSheet("background-color: rgb(170, 170, 127);")
        self.btn_tmpalamenu.setObjectName("btn_tmpalamenu")
        self.frame_soitin.raise_()
        self.frame_kanavalista.raise_()
        self.frame_raidat.raise_()
        self.frame_info.raise_()
        self.frame_alamenu.raise_()
        self.btn_tmpalamenu.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_info.setText(_translate("Form", "TextLabel"))
        self.btn_tv.setText(_translate("Form", "TV"))
        self.btn_movie.setText(_translate("Form", "Movie"))
        self.btn_subtitle.setText(_translate("Form", "Subtitle"))
        self.btn_audio.setText(_translate("Form", "Audio"))
        self.btnsulje.setText(_translate("Form", "tmpsulje"))
        self.btn_tmpalamenu.setText(_translate("Form", "tmpAlamenu"))

#################################################
        self.signal.connect(self.eventp)
        self.btn_tmpalamenu.hide()
        monitor = QtWidgets.QDesktopWidget().screenGeometry(0) #vaihda tää jos dualheadin toinen lähtö
        self.videoPlayer=None
        self.viimAudioraidat=[]
        #self.viimVideoraidat=[]
        self.viimTekstitysraidat=[]
        self.frame_info.setFixedSize(800,300)
        self.label_info.setFixedSize(800,300)
        self.frame_info.move(monitor.width()-900,50)
        self.btnsulje.clicked.connect(self.lopeta)
        self.btn_subtitle.clicked.connect(self.klikattuSmenu)
        self.btn_audio.clicked.connect(self.klikattuAmenu)
        self.btn_movie.clicked.connect(self.movieklik)
        self.btn_tv.clicked.connect(self.tvklik)
        self.btn_tmpalamenu.clicked.connect(self.nayta_alamenu)
        self.list_kohteet.clicked.connect(self.klikattuKohde)
        self.list_kohteet.itemActivated.connect(self.klikattuKohde)
        #self.list_kohteet.pressed.connect(self.kohdelistakey)
        self.list_sraidat.clicked.connect(self.klikattuSraita)
        self.list_sraidat.itemActivated.connect(self.klikattuSraita)
        self.list_araidat.clicked.connect(self.klikattuAraita)
        self.list_araidat.itemActivated.connect(self.klikattuAraita)
        Form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.CustomizeWindowHint|QtCore.Qt.FramelessWindowHint)
        self.frame_raidat.move(monitor.width()-600,monitor.height()-500-ALAMENUKORKEUS)
        self.frame_raidat.setFixedSize(500,500)
        self.frame_raidat.hide()
        self.list_sraidat.move(0,0)
        self.list_sraidat.setFixedSize(500,500)
        self.list_sraidat.hide()
        self.list_araidat.move(0,0)
        self.list_araidat.setFixedSize(500,500)
        self.list_araidat.hide()
        self.frame_soitin.setFixedSize(QtCore.QSize(monitor.width(), monitor.height()))
        self.frame_soitin.move(0,0)
        self.frame_soitin.setFixedSize(QtCore.QSize(monitor.width(), monitor.height()))
        self.frame_alamenu.setFixedSize(QtCore.QSize(monitor.width()-KANAVALISTALEVEYS,ALAMENUKORKEUS))
        self.frame_alamenu.move(KANAVALISTALEVEYS,monitor.height()-ALAMENUKORKEUS)
        #self.frame_alamenu.hide()
        self.frame_kanavalista.move(0,0)
        self.frame_kanavalista.setFixedSize(KANAVALISTALEVEYS,monitor.height())
        self.list_kohteet.move(0,0)
        self.list_kohteet.setFixedSize(KANAVALISTALEVEYS,monitor.height())
        self.frame_kanavalista.hide()
        self.striimiperus=None
        self.frame_info.hide()
        self.media = None
        self.parsed=False
        self.haeStriiminPerusosoite()
        self.tvklik()
        cec.add_callback(self.nappainPainettu, cec.EVENT_KEYPRESS)
        cec.init()
        self.seis=False
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000) 
        self.timer.timeout.connect(self.timertask)
        self.timer.start()
 

    def timertask(self):
        if self.seis:
            quit()

    def lahetanappain(self,nap):
        print(nap)

    def nappainPainettu(self, event, *args): #cec:n callback (**1**)
        print("args", args)
        if args[1] == 0 or args[0] == 69: #painike alas #69 stop lähettää vain yhden eventin
            self.signal.emit(NAPIT[args[0]]) #lähetetään signaali --> **2*

    @QtCore.pyqtSlot(str)
    def eventp(self, arvo): #(**2**)
        print(arvo)
        self.sendKey(arvo)

    def sendKey(self, nappi): #(**3**)
        print("saatu", nappi)
        if nappi=="ALAS":
            nappain=QtCore.Qt.Key_Down
        if nappi=="YLÖS":
            nappain=QtCore.Qt.Key_Up
        if nappi=="OIKEA":
            nappain=QtCore.Qt.Key_Right
        if nappi=="VASEN":
            nappain=QtCore.Qt.Key_Left
        if nappi == "OK":
            nappain=QtCore.Qt.Key_Enter

        widget = QtWidgets.QApplication.focusWidget() #aktiivinen widget
        print(widget)
        obj=widget.objectName()
        if widget == self.list_kohteet and nappi == "VASEN":
            self.frame_kanavalista.hide()
            self.frame_kanavalista.raise_()
            return
        elif nappi in ["ALAS", "YLÖS", "VASEN", "OIKEA", "OK"] and obj[:3] != "btn":
            event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, nappain, QtCore.Qt.NoModifier)
            QtCore.QCoreApplication.sendEvent(widget, event)
        elif nappi in ["VASEN", "OIKEA"] and obj[:3] == "btn":
            event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, nappain, QtCore.Qt.NoModifier)
            QtCore.QCoreApplication.sendEvent(widget, event)
        if type(widget).__name__ == "QToolButton" and nappi == "OK":
            print("space", widget.objectName())
            if obj=="btn_tv":
                self.tvklik()
            if obj=="btn_movie":
                self.movieklik()
            if obj=="btn_subtitle":
                self.klikattuSmenu()
            if obj=="btn_audio":
                self.klikattuAmenu()
            if obj=="btnsulje":
                self.lopeta()
        #elif type(widget).__name__ == "QToolButton" and nappi == "ALAS":
        elif nappi == "ALAS":
            self.frame_alamenu.hide()
            self.frame_alamenu.raise_()
        else:
            if not self.frame_alamenu.isVisible():
                self.frame_alamenu.show()

            #if isinstance(widget, PyQt5.QtWidgets.QToolButton):
            #    print("BUTTON")
    def nayta_alamenu(self):
        self.frame_alamenu.show()
        self.btn_tv.setFocus()

    def klikattuAmenu(self):
        if self.videoPlayer is None:
            return
        self.atracks=[]
        self.list_araidat.clear()
        self.frame_raidat.show()
        self.list_sraidat.hide()
        self.list_araidat.show()
        for a in self.videoPlayer.audio_get_track_description():
            self.atracks.append(a[0])
            self.list_araidat.addItem(a[1].decode())
        self.atracks.append("!close")
        self.list_araidat.addItem("[sulje]")
        self.list_araidat.setFocus()
        self.list_araidat.setCurrentRow(0)
        

    def klikattuAraita(self):
        kohde=self.list_araidat.currentRow()
        print("AKLIK", kohde)
        if self.atracks[kohde] != "!close":
            self.videoPlayer.audio_set_track(self.atracks[kohde])
        self.piilotaRaidat()

    def klikattuSmenu(self):
        if self.videoPlayer is None:
            return
        self.stracks=[]
        self.list_sraidat.clear()
        self.frame_raidat.show()
        self.list_araidat.hide()
        self.list_sraidat.show()
        for s in self.videoPlayer.video_get_spu_description():
            if [ss for ss in ["undertexter", "tekstitys", "subtitles"] if ss in s[1].decode()]:
                self.stracks.append(s[0])
                self.list_sraidat.addItem(s[1].decode())
        self.stracks.append("!close")
        self.list_sraidat.addItem("[sulje]")
        self.list_sraidat.setFocus()
        self.list_sraidat.setCurrentRow(0)

    def klikattuSraita(self):
        kohde=self.list_sraidat.currentRow()
        print("sKLIK", kohde)
        if self.stracks[kohde] != "!close":
            self.videoPlayer.video_set_spu(self.stracks[kohde])
        self.piilotaRaidat()


    def piilotaRaidat(self):
        self.frame_raidat.hide()
        self.frame_raidat.raise_()
        self.frame_alamenu.hide()
        self.frame_alamenu.raise_()
        self.btn_tv.setFocus()


    def movieklik(self): 
        self.list_kohteet.clear()
        self.striimiLista=[]
        self.striimiLista.append(["<--", "exit"])
        qitem=QtWidgets.QListWidgetItem("<--")
        qitem.setForeground(QtGui.QColor("red"))
        self.list_kohteet.addItem(qitem)
        self.frame_kanavalista.show()
        self.list_kohteet.setFocus()
        self.list_kohteet.setCurrentRow(0)
        url = ENIGMAURL+"/api/movielist" 
        r=requests.get(url)
        data = r.json()
        basedir = data["directory"]
        for d in data["movies"]:
            #self.kanavavalikko.addItem(d["filename_stripped"])
            qitem=QtWidgets.QListWidgetItem(d["filename_stripped"])
            qitem.setForeground(QtGui.QColor("bisque"))
            self.list_kohteet.addItem(qitem)
            self.striimiLista.append([d["filename_stripped"] , d["serviceref"]])
        alihakemistot=data["bookmarks"]
        for ali in alihakemistot:
            qitem=QtWidgets.QListWidgetItem("***" + ali + "***")
            qitem.setForeground(QtGui.QColor("silver"))
            self.list_kohteet.addItem(qitem)
            self.striimiLista.append(["***" + ali + "***", ""])
            url = ENIGMAURL+"/api/movielist?dirname="+basedir+ali
            r=requests.get(url)
            data = r.json()
            for d in data["movies"]:
                print(d)
                qitem=QtWidgets.QListWidgetItem(d["filename_stripped"])
                qitem.setForeground(QtGui.QColor("bisque"))
                self.list_kohteet.addItem(qitem)
                self.striimiLista.append([d["filename_stripped"] , d["serviceref"]])

    def tvklik(self):
        self.list_kohteet.clear()
        self.striimiLista=[]
        self.striimiLista.append(["<--", "exit"])
        qitem=QtWidgets.QListWidgetItem("<--")
        qitem.setForeground(QtGui.QColor("red"))
        self.list_kohteet.addItem(qitem)
        self.frame_kanavalista.show()
        self.list_kohteet.setFocus()
        self.list_kohteet.setCurrentRow(0)
        url = ENIGMAURL+"/api/getallservices" 
        r=requests.get(url)
        data = r.json()
        for palvelut in data["services"]:
            qitem=QtWidgets.QListWidgetItem(palvelut["servicename"])
            qitem.setForeground(QtGui.QColor("silver"))
            self.list_kohteet.addItem(qitem)
            self.striimiLista.append([palvelut["servicename"] , ""])
            for alipalvelu in palvelut["subservices"]:
                qitem=QtWidgets.QListWidgetItem(alipalvelu["servicename"])
                if alipalvelu["servicereference"].startswith("1:64"): #väliotsikko
                    qitem.setForeground(QtGui.QColor("silver"))
                else:
                    qitem.setForeground(QtGui.QColor("bisque"))
                self.list_kohteet.addItem(qitem)
                self.striimiLista.append([alipalvelu["servicename"] , alipalvelu["servicereference"]])

    def naytaSubs(self):
        self.list_araidat.hide()
        self.list_sraidat.show()
        self.frame_raidat.show()

    def naytaAudio(self):
        self.list_sraidat.hide()
        self.list_araidat.show()
        self.frame_raidat.show()

    def haeStriiminPerusosoite(self):
        url= ENIGMAURL+"/api/stream.m3u" #hae striimien perus-osoite
        print(url)
        r=requests.get(url)
        vast=r.text
        surl=vast.split("\n")[-2]
        if salasana is not None:
            alku, loppu=surl.split("://")
            surl=alku+"://"+kayttaja+":"+salasana+"@"+loppu
        self.striimiperus=surl


    def klikattuKohde(self):
        kohde=self.list_kohteet.currentRow()
        print("klikattukohde",kohde, self.striimiLista[kohde])
        if kohde==0: #exit ekana
            #self.list_kohteet.hide()
            self.frame_kanavalista.hide()
            self.frame_kanavalista.raise_()
            self.nayta_alamenu()
        self.label_info.setText(self.striimiLista[kohde][0])
        #self.toistaUrl(kohde)
        self.frame_kanavalista.hide()
        if self.videoPlayer is not None:
            self.destroyVlc()
        soittourl=self.striimiperus+urllib.parse.quote(self.striimiLista[kohde][1])
        print("SOITA", soittourl)
        self.frame_alamenu.hide()
        self.label_info.setText(self.striimiLista[kohde][0]+"\n"+soittourl)
        #opts=['--vbi-opaque', '--vbi-text', '--freetype-color=16776960', '--freetype-background-opacity=128', '--freetype-shadow-opacity=0', '--freetype-background-color=0', '--freetype-font=Tiresias Infofont', 
        #        '--text-renderer=any', '--freetype-rel-fontsize=-5']
        opts=['--video-on-top', '--vbi-opaque', '--vbi-text', '--freetype-color=16776960', '--freetype-background-opacity=128', '--freetype-shadow-opacity=0', '--freetype-background-color=0', '--freetype-font=Tiresias Infofont', 
               '--sub-text-scale=50', '--sub-margin=20']
        self.vlcInstance = vlc.Instance(opts)
        self.videoPlayer = self.vlcInstance.media_player_new()
        self.media = self.vlcInstance.media_new(soittourl)
        self.videoPlayer.set_media(self.media)
        self.videoPlayer.play()
        self.videoPlayer.set_xwindow(self.frame_soitin.winId())


    def destroyVlc(self):
        print("TUHOA")
        self.videoPlayer.release()

    def lopeta(self):
        self.seis=True


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    #Form.show()
    Form.showMaximized()
    sys.exit(app.exec_())

