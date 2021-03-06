#!/usr/bin/env python3

KANAVALISTALEVEYS=650
ALAPALKKIKORKEUS=80
NAPIT = {1: "YLÖS", 0: "OK", 2: "ALAS", 3: "VASEN", 4: "OIKEA", 13: "BACK", 69: "STOP", 70: "PAUSE", 72: "REV", 73: "FWD", 68: "PLAY"}

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
import subprocess, signal

def debug(*args):
    pass
    #print(args)

home = str(Path.home())
debug(home)
if not os.path.exists(home+"/.config/pycectv.conf"):
    debug("konfiguraatiotiedosto ~/.config/pycectv.conf puuttuu!")
    quit()
config=ConfigObj(home+"/.config/pycectv.conf")
ENIGMAURL=config.get("enigmaurl")
if len(ENIGMAURL)<5:
    debug("enigmaurl puuttuu asetustiedostosta")
    quit()
kayttaja=config.get("user")
salasana=config.get("pass")

if salasana is not None:
    alku,loppu=ENIGMAURL.split("://") 
    ENIGMAURL=alku+"://"+kayttaja+":"+salasana+"@"+loppu


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(QtCore.QObject):
    signal = QtCore.pyqtSignal([str])
#################################################

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(852, 649)
        Form.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border: none;")
        self.frame_alapalkki = QtWidgets.QFrame(Form)
        self.frame_alapalkki.setGeometry(QtCore.QRect(50, 560, 800, 81))
        self.frame_alapalkki.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_alapalkki.setStyleSheet("background-color: rgb(0, 0, 255);")
        self.frame_alapalkki.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_alapalkki.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_alapalkki.setObjectName("frame_alapalkki")
        self.btn_tv = QtWidgets.QToolButton(self.frame_alapalkki)
        self.btn_tv.setGeometry(QtCore.QRect(0, 10, 100, 51))
        self.btn_tv.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 18pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_tv.setObjectName("btn_tv")
        self.btn_tallenne = QtWidgets.QToolButton(self.frame_alapalkki)
        self.btn_tallenne.setGeometry(QtCore.QRect(220, 10, 100, 51))
        self.btn_tallenne.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 18pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_tallenne.setObjectName("btn_tallenne")
        self.btn_teksti = QtWidgets.QToolButton(self.frame_alapalkki)
        self.btn_teksti.setGeometry(QtCore.QRect(330, 10, 100, 51))
        self.btn_teksti.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 18pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_teksti.setObjectName("btn_teksti")
        self.btn_aani = QtWidgets.QToolButton(self.frame_alapalkki)
        self.btn_aani.setGeometry(QtCore.QRect(440, 10, 100, 51))
        self.btn_aani.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 18pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_aani.setObjectName("btn_aani")
        self.btn_sulje = QtWidgets.QToolButton(self.frame_alapalkki)
        self.btn_sulje.setGeometry(QtCore.QRect(550, 10, 100, 51))
        self.btn_sulje.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 18pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_sulje.setObjectName("btn_sulje")
        self.btn_oma = QtWidgets.QToolButton(self.frame_alapalkki)
        self.btn_oma.setGeometry(QtCore.QRect(110, 10, 100, 51))
        self.btn_oma.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 18pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_oma.setObjectName("btn_oma")
        self.list_ohjelma = QtWidgets.QListWidget(Form)
        self.list_ohjelma.setGeometry(QtCore.QRect(10, 20, 141, 431))
        self.list_ohjelma.setFocusPolicy(QtCore.Qt.NoFocus)
        self.list_ohjelma.setStyleSheet("QListView{\n"
"background-color:rgb(41, 85, 74); \n"
"font: 18pt \"Ubuntu\";\n"
"color: white;}\n"
"\n"
"QListView::item:selected{\n"
"background-color: rgb(75,153,134); \n"
"color: yellow;};")
        self.list_ohjelma.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_ohjelma.setObjectName("list_ohjelma")
        self.frame_soitin = QtWidgets.QFrame(Form)
        self.frame_soitin.setGeometry(QtCore.QRect(320, 90, 351, 191))
        self.frame_soitin.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_soitin.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_soitin.setObjectName("frame_soitin")
        self.frame_tracktausta = QtWidgets.QFrame(Form)
        self.frame_tracktausta.setGeometry(QtCore.QRect(430, 330, 281, 211))
        self.frame_tracktausta.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.frame_tracktausta.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_tracktausta.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tracktausta.setObjectName("frame_tracktausta")
        self.list_tekstitys = QtWidgets.QListWidget(Form)
        self.list_tekstitys.setGeometry(QtCore.QRect(280, 410, 81, 81))
        self.list_tekstitys.setFocusPolicy(QtCore.Qt.NoFocus)
        self.list_tekstitys.setStyleSheet("QListView{\n"
"background-color:rgb(41, 85, 74); \n"
"font: 18pt \"Ubuntu\";\n"
"color: white;}\n"
"\n"
"QListView::item:selected{\n"
"background-color: rgb(75,153,134); \n"
"color: yellow;};")
        self.list_tekstitys.setObjectName("list_tekstitys")
        self.list_aani = QtWidgets.QListWidget(Form)
        self.list_aani.setGeometry(QtCore.QRect(760, 410, 51, 71))
        self.list_aani.setFocusPolicy(QtCore.Qt.NoFocus)
        self.list_aani.setStyleSheet("QListView{\n"
"background-color:rgb(41, 85, 74); \n"
"font: 18pt \"Ubuntu\";\n"
"color: white;}\n"
"\n"
"QListView::item:selected{\n"
"background-color: rgb(75,153,134); \n"
"color: yellow;};")
        self.list_aani.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_aani.setObjectName("list_aani")
        self.list_ulos = QtWidgets.QListWidget(Form)
        self.list_ulos.setGeometry(QtCore.QRect(320, 320, 81, 81))
        self.list_ulos.setFocusPolicy(QtCore.Qt.NoFocus)
        self.list_ulos.setStyleSheet("QListView{\n"
"background-color:rgb(41, 85, 74); \n"
"font: 18pt \"Ubuntu\";\n"
"color: white;}\n"
"\n"
"QListView::item:selected{\n"
"background-color: rgb(75,153,134); \n"
"color: yellow;};")
        self.list_ulos.setObjectName("list_ulos")
        self.list_omat = QtWidgets.QListWidget(Form)
        self.list_omat.setGeometry(QtCore.QRect(740, 250, 81, 81))
        self.list_omat.setFocusPolicy(QtCore.Qt.NoFocus)
        self.list_omat.setStyleSheet("QListView{\n"
"background-color:rgb(41, 85, 74); \n"
"font: 18pt \"Ubuntu\";\n"
"color: white;}\n"
"\n"
"QListView::item:selected{\n"
"background-color: rgb(75,153,134); \n"
"color: yellow;};")
        self.list_omat.setObjectName("list_omat")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.btn_tv, self.btn_oma)
        Form.setTabOrder(self.btn_oma, self.btn_tallenne)
        Form.setTabOrder(self.btn_tallenne, self.btn_teksti)
        Form.setTabOrder(self.btn_teksti, self.btn_aani)
        Form.setTabOrder(self.btn_aani, self.btn_sulje)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_tv.setText(_translate("Form", "TV"))
        self.btn_tallenne.setText(_translate("Form", "Tallenne"))
        self.btn_teksti.setText(_translate("Form", "Teksti"))
        self.btn_aani.setText(_translate("Form", "Ääni"))
        self.btn_sulje.setText(_translate("Form", "Ulos"))
        self.btn_oma.setText(_translate("Form", "Oma"))


#################################################
        Form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.CustomizeWindowHint|QtCore.Qt.FramelessWindowHint)
        self.monitor = QtWidgets.QDesktopWidget().screenGeometry(0) # Jos useampi monitori käytössä
        self.frame_soitin.move(KANAVALISTALEVEYS,0)
        self.frame_soitin.setFixedSize(self.monitor.width()-KANAVALISTALEVEYS,self.monitor.height()-ALAPALKKIKORKEUS)
        self.frame_alapalkki.move(KANAVALISTALEVEYS,self.monitor.height()-ALAPALKKIKORKEUS)
        self.frame_alapalkki.setFixedSize(self.monitor.width()-KANAVALISTALEVEYS,ALAPALKKIKORKEUS)
        self.list_aani.setFixedSize(500,500)
        self.list_aani.move(self.monitor.width()-520,self.monitor.height()-ALAPALKKIKORKEUS-510)
        self.list_aani.hide()
        self.frame_tracktausta.setFixedSize(500,500)
        self.frame_tracktausta.move(self.monitor.width()-520,self.monitor.height()-ALAPALKKIKORKEUS-510)
        self.frame_tracktausta.hide()
        self.list_tekstitys.setFixedSize(500,500)
        self.list_tekstitys.move(self.monitor.width()-520,self.monitor.height()-ALAPALKKIKORKEUS-510)
        self.list_tekstitys.hide()
        self.list_ulos.setFixedSize(500,500)
        self.list_ulos.move(self.monitor.width()-520,self.monitor.height()-ALAPALKKIKORKEUS-510)
        self.list_ulos.hide()
        self.list_omat.setFixedSize(500,500)
        self.list_omat.move(self.monitor.width()-520,self.monitor.height()-ALAPALKKIKORKEUS-510)
        self.list_omat.hide()
        self.list_ohjelma.move(0,0)
        self.list_ohjelma.setFixedSize(KANAVALISTALEVEYS,self.monitor.height())
        self.list_ohjelma.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_aani.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_tekstitys.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_ohjelma.clicked.connect(self.klikattuKohde)
        self.list_ohjelma.itemActivated.connect(self.klikattuKohde)
        self.haeStriiminPerusosoite()
        self.videoPlayer=None
        self.btn_tv.clicked.connect(self.tvklik)
        self.btn_aani.clicked.connect(self.klikattuAmenu)
        self.btn_oma.clicked.connect(self.klikattuOmenu)
        self.btn_sulje.clicked.connect(self.klikattuUmenu)
        self.list_aani.clicked.connect(self.klikattuAraita)
        self.list_aani.itemActivated.connect(self.klikattuAraita)
        self.btn_teksti.clicked.connect(self.klikattuSmenu)
        self.list_tekstitys.clicked.connect(self.klikattuSraita)
        self.list_tekstitys.itemActivated.connect(self.klikattuSraita)
        self.list_ulos.clicked.connect(self.klikattuUraita)
        self.list_ulos.itemActivated.connect(self.klikattuUraita)
        self.list_omat.clicked.connect(self.klikattuOraita)
        self.list_omat.itemActivated.connect(self.klikattuOraita)
        self.btn_tallenne.clicked.connect(self.movieklik)
        self.tvklik()
        cec.add_callback(self.cecNappain, cec.EVENT_KEYPRESS)
        cec.init()
        self.nappain=None
        self.seis=False
        self.signal.connect(self.eventp)
        self.omaPaalla=None # silloin kun oma-valikon skripti on päällä, tässä sen subprocess ja voidaan tappaa STOP-painikkeella
        self.tallenneToistuu=None # Kun tallenne toistuu, pause ja kelaus on aktiivisia !TODO

    def cecNappain(self, event, *args): #cec:n callback (**1**)
        debug("args", args)
        if args[1] == 0 or args[0] == 69: #painike alas #69 stop lähettää vain yhden eventin
            self.signal.emit(NAPIT[args[0]]) #lähetetään signaali --> **2*

    @QtCore.pyqtSlot(str)
    def eventp(self, arvo): #(**2**)
        debug(arvo)
        self.sendKey(arvo)

    def sendKey(self, nappi): #(**3**)
        debug("saatu", nappi)
        if self.omaPaalla is not None: #jos oma ulkoinen skripti päällä
            if nappi in ["STOP", "BACK"]: #pysäytetään oma skripti
                debug("tapetaan oma")
                os.killpg(os.getpgid(self.omaPaalla.pid), signal.SIGTERM) 
                self.omaPaalla=None
                Form.showMaximized()
            return
        elif self.tallenneToistuu: # tallenne on toistumassa
            if nappi in ["PAUSE", "REV", "FWD", "PLAY"]: # ohjataan tallennetta
                pass #!TODO
                return
        if nappi=="ALAS":
            nappain=QtCore.Qt.Key_Down
        elif nappi=="YLÖS":
            nappain=QtCore.Qt.Key_Up
        elif nappi=="OIKEA":
            nappain=QtCore.Qt.Key_Right
        elif nappi=="VASEN":
            nappain=QtCore.Qt.Key_Left
        elif nappi == "OK":
            nappain=QtCore.Qt.Key_Enter
        elif nappi == "BACK":
            nappain=QtCore.Qt.Key_Escape
        widget = QtWidgets.QApplication.focusWidget() #aktiivinen widget
        obj=widget.objectName() #aktiivisen widgetin nimi
        debug("widget",widget, obj)
        if widget == self.list_ohjelma and self.list_ohjelma.isVisible():
            if nappi in ["YLÖS", "ALAS", "OK"]:
                event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, nappain, QtCore.Qt.NoModifier)
                QtCore.QCoreApplication.sendEvent(widget, event)
            elif nappi in ["VASEN", "BACK"]: #piilota kanavalista
                self.list_ohjelma.hide()
                self.frame_soitin.move(0,0)
                self.frame_soitin.setFixedSize(self.monitor.width(),self.monitor.height())
                self.alapalkkiShow()
        elif nappi in ["OK", "YLÖS"] and obj[:3] == "btn" and self.frame_alapalkki.isVisible():
            widget.click()
        elif nappi in ["ALAS", "BACK"] and obj[:3] == "btn":
            self.alapalkkiHide()
        elif nappi in ["VASEN", "OIKEA"] and obj[:3] == "btn":
            event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, nappain, QtCore.Qt.NoModifier)
            QtCore.QCoreApplication.sendEvent(widget, event)
        elif nappi in ["YLÖS", "BACK"] and not self.frame_alapalkki.isVisible():
            debug("alapalkkishow")
            self.alapalkkiShow()
        elif obj in ["list_tekstitys", "list_aani", "list_ulos", "list_omat"]:
            if nappi in ["YLÖS", "ALAS", "OK"]:
                event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, nappain, QtCore.Qt.NoModifier)
                QtCore.QCoreApplication.sendEvent(widget, event)
            # elif nappi == "BACK":
            #     widget.hide()
            #     self.alapalkkiHide()
            
    def klikattuUmenu(self):
        self.utracks=[]
        self.list_ulos.clear()
        self.list_ulos.show()
        self.frame_tracktausta.show()
        self.utracks.append("!stop")
        self.list_ulos.addItem("Pysäytä VLC")
        self.utracks.append("!reboot")
        self.list_ulos.addItem("Reboot")
        self.utracks.append("!halt")
        self.list_ulos.addItem("Sammuta")
        self.utracks.append("!exit")
        self.list_ulos.addItem("Lopeta")
        self.utracks.append("!close")
        self.list_ulos.addItem("[sulje]")
        self.list_ulos.setFocus()
        self.list_ulos.setCurrentRow(0)


    def klikattuUraita(self):
        kohde=self.list_ulos.currentRow()
        if self.utracks[kohde]=="!reboot":
            os.system("sudo reboot")
        elif self.utracks[kohde]=="!halt":
            os.system("sudo halt")
        elif self.utracks[kohde]=="!exit":
            quit()
        elif self.utracks[kohde]=="!halt":
            os.system("sudo halt")
        elif self.utracks[kohde]=="!stop":
            if self.videoPlayer is not None:
                self.videoPlayer.release()
        self.list_ulos.hide()
        self.frame_tracktausta.hide()
        self.alapalkkiHide()

    def klikattuAmenu(self):
        if self.videoPlayer is None:
            return
        self.atracks=[]
        self.list_aani.clear()
        self.list_aani.show()
        self.frame_tracktausta.show()
        for a in self.videoPlayer.audio_get_track_description():
            self.atracks.append(a[0])
            self.list_aani.addItem(a[1].decode())
        self.atracks.append("!close")
        self.list_aani.addItem("[sulje]")
        self.list_aani.setFocus()
        self.list_aani.setCurrentRow(0)

    def klikattuAraita(self):
        kohde=self.list_aani.currentRow()
        debug("AKLIK", kohde)
        if self.atracks[kohde] != "!close":
            self.videoPlayer.audio_set_track(self.atracks[kohde])
        self.list_aani.hide()
        self.alapalkkiHide()
        self.frame_tracktausta.hide()

    def klikattuSmenu(self):
        if self.videoPlayer is None:
            return
        self.stracks=[]
        self.list_tekstitys.clear()
        self.list_tekstitys.show()
        self.frame_tracktausta.show()
        self.list_tekstitys.addItem("Pois")
        self.stracks.append(-1)
        for s in self.videoPlayer.video_get_spu_description():
            if [ss for ss in ["undertexter", "tekstitys", "subtitles"] if ss in s[1].decode()]:
                self.stracks.append(s[0])
                self.list_tekstitys.addItem(s[1].decode())
        self.stracks.append("!close")
        self.list_tekstitys.addItem("[sulje]")
        self.list_tekstitys.setFocus()
        self.list_tekstitys.setCurrentRow(0)


    def klikattuSraita(self):
        kohde=self.list_tekstitys.currentRow()
        debug("sKLIK", kohde)
        if self.stracks[kohde] != "!close":
            self.videoPlayer.video_set_spu(self.stracks[kohde])
        self.list_tekstitys.hide()
        self.frame_tracktausta.hide()
        self.alapalkkiHide()

    def alapalkkiHide(self):
        #self.frame_soitin.setFixedSize(self.monitor.width(),self.monitor.height())
        #self.frame_soitin.move(0,0)
        self.frame_alapalkki.hide()

    def alapalkkiShow(self):
        #self.frame_soitin.setFixedSize(self.monitor.width(),self.monitor.height()-ALAPALKKIKORKEUS)
        #self.frame_soitin.move(0,0)
        self.frame_alapalkki.show()
        self.frame_alapalkki.raise_()
        self.btn_tv.setFocus()


    def klikattuOmenu(self): #omat skripti kohteesta ~/pycectv jos niitä on..
        skriptihakemisto= os.path.expanduser("~")+"/pycectv"
        if not os.path.isdir(skriptihakemisto):
            debug("ei ole skriptihakemistoa",skriptihakemisto)
            return
        self.otracks=[]
        self.list_omat.clear()
        self.list_omat.show()
        self.frame_tracktausta.show()
        filut=os.listdir(skriptihakemisto)
        for filu in filut:
            self.otracks.append(filu)
            self.list_omat.addItem(filu)
        self.otracks.append("!close")
        self.list_omat.addItem("[sulje]")
        self.list_omat.setFocus()
        self.list_omat.setCurrentRow(0)

    def klikattuOraita(self):
        kohde=self.list_omat.currentRow()
        debug("omaKLIK", kohde, self.otracks[kohde])
        if self.otracks[kohde]=="!close":
            self.list_omat.hide()
            self.frame_tracktausta.hide()
            self.alapalkkiHide()
            return
        else:
            Form.hide()
            komento= os.path.expanduser("~")+"/pycectv/"+self.otracks[kohde]
            self.omaPaalla = subprocess.Popen(komento, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid) 
            debug("PID",self.omaPaalla.pid)


    def tvklik(self):
        self.frame_soitin.setFixedSize(self.monitor.width()-KANAVALISTALEVEYS,self.monitor.height())
        self.frame_soitin.move(KANAVALISTALEVEYS,0)
        self.frame_alapalkki.hide()
        self.list_ohjelma.clear()
        self.striimiLista=[]
        # self.striimiLista.append(["<--", "exit"]) #ei tätä tartte kun back-painike kätevämpi
        # qitem=QtWidgets.QListWidgetItem("<--")
        # qitem.setForeground(QtGui.QColor("red"))
        # self.list_ohjelma.addItem(qitem)
        self.list_ohjelma.show()
        self.list_ohjelma.setFocus()
        self.list_ohjelma.setCurrentRow(0)
        url = ENIGMAURL+"/api/getallservices" 
        r=requests.get(url)
        data = r.json()
        for palvelut in data["services"]:
            qitem=QtWidgets.QListWidgetItem(palvelut["servicename"])
            qitem.setForeground(QtGui.QColor("silver"))
            self.list_ohjelma.addItem(qitem)
            self.striimiLista.append([palvelut["servicename"] , ""])
            for alipalvelu in palvelut["subservices"]:
                qitem=QtWidgets.QListWidgetItem(alipalvelu["servicename"])
                if alipalvelu["servicereference"].startswith("1:64"): #väliotsikko
                    qitem.setForeground(QtGui.QColor("silver"))
                else:
                    qitem.setForeground(QtGui.QColor("bisque"))
                self.list_ohjelma.addItem(qitem)
                self.striimiLista.append([alipalvelu["servicename"] , alipalvelu["servicereference"]])

    def movieklik(self): 
        self.frame_soitin.setFixedSize(self.monitor.width()-KANAVALISTALEVEYS,self.monitor.height())
        self.frame_soitin.move(KANAVALISTALEVEYS,0)
        self.frame_alapalkki.hide()
        self.list_ohjelma.clear()
        self.striimiLista=[]
        self.striimiLista.append(["<--", "exit"])
        qitem=QtWidgets.QListWidgetItem("<--")
        qitem.setForeground(QtGui.QColor("red"))
        self.list_ohjelma.addItem(qitem)
        self.list_ohjelma.show()
        self.list_ohjelma.setFocus()
        self.list_ohjelma.setCurrentRow(0)
        url = ENIGMAURL+"/api/movielist" 
        r=requests.get(url)
        data = r.json()
        basedir = data["directory"]
        for d in data["movies"]:
            #self.kanavavalikko.addItem(d["filename_stripped"])
            qitem=QtWidgets.QListWidgetItem(d["filename_stripped"])
            qitem.setForeground(QtGui.QColor("bisque"))
            self.list_ohjelma.addItem(qitem)
            self.striimiLista.append([d["filename_stripped"] , d["serviceref"]])
        alihakemistot=data["bookmarks"]
        for ali in alihakemistot:
            qitem=QtWidgets.QListWidgetItem("***" + ali + "***")
            qitem.setForeground(QtGui.QColor("silver"))
            self.list_ohjelma.addItem(qitem)
            self.striimiLista.append(["***" + ali + "***", ""])
            url = ENIGMAURL+"/api/movielist?dirname="+basedir+ali
            r=requests.get(url)
            data = r.json()
            for d in data["movies"]:
                debug(d)
                qitem=QtWidgets.QListWidgetItem(d["filename_stripped"])
                qitem.setForeground(QtGui.QColor("bisque"))
                self.list_ohjelma.addItem(qitem)
                self.striimiLista.append([d["filename_stripped"] , d["serviceref"]])


    def klikattuKohde(self): #kanavalistalta klikattu ohjelmaa
        self.frame_soitin.move(0,0)
        self.frame_soitin.setFixedSize(self.monitor.width(),self.monitor.height())
        kohde=self.list_ohjelma.currentRow()
        debug("klikattukohde",kohde, self.striimiLista[kohde])
        self.list_ohjelma.hide()
        if kohde==0: #exit ekana
            return
        if self.videoPlayer is not None:
            self.videoPlayer.release()
        soittourl=self.striimiperus+urllib.parse.quote(self.striimiLista[kohde][1])
        debug("SOITA", soittourl)
        self.frame_alapalkki.hide()
        #opts=['--vbi-opaque', '--vbi-text', '--freetype-color=16776960', '--freetype-background-opacity=128', '--freetype-shadow-opacity=0', '--freetype-background-color=0', '--freetype-font=Tiresias Infofont', 
        #        '--text-renderer=any', '--freetype-rel-fontsize=-5']
        opts=['--video-on-top', '--vbi-opaque', '--vbi-text', '--freetype-color=16776960', '--freetype-background-opacity=128', '--freetype-shadow-opacity=0', '--freetype-background-color=0', '--freetype-font=Tiresias Infofont', 
               '--sub-text-scale=60', '--sub-margin=20']
        self.vlcInstance = vlc.Instance(opts)
        self.videoPlayer = self.vlcInstance.media_player_new()
        self.media = self.vlcInstance.media_new(soittourl)
        self.videoPlayer.set_media(self.media)
        self.videoPlayer.play()
        self.videoPlayer.set_xwindow(self.frame_soitin.winId())

        
    def haeStriiminPerusosoite(self):
        url= ENIGMAURL+"/api/stream.m3u" #hae striimien perus-osoite
        debug(url)
        r=requests.get(url)
        vast=r.text
        surl=vast.split("\n")[-2]
        if salasana is not None:
            alku, loppu=surl.split("://")
            surl=alku+"://"+kayttaja+":"+salasana+"@"+loppu
        self.striimiperus=surl

    def lopeta(self):
        if self.videoPlayer is not None:
            self.videoPlayer.release()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.showMaximized()
    sys.exit(app.exec_())
