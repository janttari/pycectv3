#!/usr/bin/env python3

KANAVALISTALEVEYS=650
NAPIT = {1: "YLÖS", 0: "OK", 2: "ALAS", 3: "VASEN", 4: "OIKEA", 13: "BACK", 69: "STOP", 70: "PAUSE", 72: "REV", 73: "FWD", 68: "PLAY"}

#menu-kohteiden tyypit:
TRACKAUDIO=0
TRACKTEKSTITYS=1
TRACKOMA=2
TRACKTOIMINNOT=3

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

def haekieli(kieli): #Tää probleema poistuu VLC4 myötä onneksi :D
    KIELET=[
["fin", "suomi", "finska", "finnish"],
["swe", "ruotsi", "svenska", "swedish"],
["eng", "englanti", "engelska", "english"],
["nor", "norja", "norska", "norwegian"],
["dan", "tanska", "danska", "danish"],
["dut", "hollanti", "holländska", "dutch"]
]
    for k in KIELET:
        if kieli in k:
            return k[0]

from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_Form(QtCore.QObject):
    signal = QtCore.pyqtSignal([str])
#################################################

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(873, 566)
        self.frame_ala = QtWidgets.QFrame(Form)
        self.frame_ala.setGeometry(QtCore.QRect(190, 490, 670, 70))
        self.frame_ala.setStyleSheet("background-color: rgb(85, 85, 255);")
        self.frame_ala.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ala.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ala.setObjectName("frame_ala")
        self.btn_tv = QtWidgets.QToolButton(self.frame_ala)
        self.btn_tv.setGeometry(QtCore.QRect(10, 10, 100, 50))
        self.btn_tv.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 16pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_tv.setObjectName("btn_tv")
        self.btn_tallenne = QtWidgets.QToolButton(self.frame_ala)
        self.btn_tallenne.setGeometry(QtCore.QRect(120, 10, 100, 50))
        self.btn_tallenne.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 16pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_tallenne.setObjectName("btn_tallenne")
        self.btn_teksti = QtWidgets.QToolButton(self.frame_ala)
        self.btn_teksti.setGeometry(QtCore.QRect(230, 10, 100, 50))
        self.btn_teksti.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 16pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_teksti.setObjectName("btn_teksti")
        self.btn_aani = QtWidgets.QToolButton(self.frame_ala)
        self.btn_aani.setGeometry(QtCore.QRect(340, 10, 100, 50))
        self.btn_aani.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 16pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_aani.setObjectName("btn_aani")
        self.btn_oma = QtWidgets.QToolButton(self.frame_ala)
        self.btn_oma.setGeometry(QtCore.QRect(450, 10, 100, 50))
        self.btn_oma.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 16pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_oma.setObjectName("btn_oma")
        self.btn_toiminnot = QtWidgets.QToolButton(self.frame_ala)
        self.btn_toiminnot.setGeometry(QtCore.QRect(560, 10, 100, 50))
        self.btn_toiminnot.setStyleSheet("QToolButton{\n"
"background-color: rgb(0,0,255);\n"
"font: 16pt \"Ubuntu\";\n"
"color: yellow;}\n"
"\n"
"QToolButton::focus{\n"
"border-top-right-radius: 0px;\n"
"background-color: rgb(255,0,0); \n"
"color: yellow;};")
        self.btn_toiminnot.setObjectName("btn_toiminnot")
        self.frame_raitatausta = QtWidgets.QFrame(Form)
        self.frame_raitatausta.setGeometry(QtCore.QRect(650, 30, 191, 201))
        self.frame_raitatausta.setStyleSheet("background-color: rgb(0, 170, 127);")
        self.frame_raitatausta.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_raitatausta.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_raitatausta.setObjectName("frame_raitatausta")
        self.list_menu = QtWidgets.QListWidget(self.frame_raitatausta)
        self.list_menu.setGeometry(QtCore.QRect(20, 20, 151, 141))
        self.list_menu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.list_menu.setStyleSheet("QListView{\n"
"background-color:rgb(41, 85, 74); \n"
"font: 18pt \"Ubuntu\";\n"
"color: white;}\n"
"\n"
"QListView::item:selected{\n"
"background-color: rgb(75,153,134); \n"
"color: yellow;};")
        self.list_menu.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_menu.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_menu.setObjectName("list_menu")
        self.frame_video = QtWidgets.QFrame(Form)
        self.frame_video.setGeometry(QtCore.QRect(340, 20, 241, 161))
        self.frame_video.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame_video.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_video.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_video.setObjectName("frame_video")
        self.frame_ohjelma = QtWidgets.QFrame(Form)
        self.frame_ohjelma.setGeometry(QtCore.QRect(10, 10, 300, 493))
        self.frame_ohjelma.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frame_ohjelma.setStyleSheet("background-color: rgb(0, 170, 127);")
        self.frame_ohjelma.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ohjelma.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ohjelma.setObjectName("frame_ohjelma")
        self.list_ohjelma = QtWidgets.QListWidget(self.frame_ohjelma)
        self.list_ohjelma.setGeometry(QtCore.QRect(120, 100, 131, 192))
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
        self.list_ohjelma.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_ohjelma.setObjectName("list_ohjelma")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_tv.setText(_translate("Form", "TV"))
        self.btn_tallenne.setText(_translate("Form", "Tallenne"))
        self.btn_teksti.setText(_translate("Form", "Teksti"))
        self.btn_aani.setText(_translate("Form", "Ääni"))
        self.btn_oma.setText(_translate("Form", "Oma"))
        self.btn_toiminnot.setText(_translate("Form", "Menu"))



#################################################

        Form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.CustomizeWindowHint|QtCore.Qt.FramelessWindowHint)
        self.monitor = QtWidgets.QDesktopWidget().screenGeometry(0) # Jos useampi monitori käytössä vaihda
        self.list_ohjelma.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_ohjelma.clicked.connect(self.klikattuKohde)
        self.list_ohjelma.itemActivated.connect(self.klikattuKohde)
        self.haeStriiminPerusosoite()
        self.videoPlayer=None
        self.btn_tv.clicked.connect(self.tvklik)
        self.btn_aani.clicked.connect(lambda: self.klikattumenu(TRACKAUDIO))
        self.list_menu.clicked.connect(self.klikatturaita)
        self.list_menu.itemActivated.connect(self.klikatturaita)
        self.btn_teksti.clicked.connect(lambda: self.klikattumenu(TRACKTEKSTITYS))
        self.btn_toiminnot.clicked.connect(lambda: self.klikattumenu(TRACKTOIMINNOT))
        self.btn_oma.clicked.connect(lambda: self.klikattumenu(TRACKOMA))
        self.btn_tallenne.clicked.connect(self.movieklik)
        cec.add_callback(self.cecNappain, cec.EVENT_KEYPRESS)
        cec.init()
        self.nappain=None
        self.seis=False
        self.signal.connect(self.eventp)
        self.frame_ala.move(self.monitor.width()-self.frame_ala.width(),self.monitor.height()-self.frame_ala.height())
        self.frame_raitatausta.setFixedSize(500,500)
        self.frame_raitatausta.move(self.monitor.width()-self.frame_raitatausta.width()-20,self.monitor.height()-self.frame_raitatausta.height()-self.frame_ala.height())
        self.frame_raitatausta.hide()
        self.list_menu.setFixedSize(500,500)
        self.list_menu.move(0,0)
        self.frame_ohjelma.setFixedSize(KANAVALISTALEVEYS,self.monitor.height())
        self.frame_ohjelma.move(0,0)
        self.list_ohjelma.setFixedSize(KANAVALISTALEVEYS,self.monitor.height())
        self.list_ohjelma.move(0,0)
        self.omaProsessi=None #oma skripti päällä?
        self.tallenneToistuu=None #Tallenteen toistuessa pause ja pikakelaus mahdollista
        self.timerAutoraita=QtCore.QTimer()
        self.timerAutoraita.setInterval(5000)
        self.timerAutoraita.timeout.connect(self.autoRaidat)
        self.kanavalistatyyppi=0 #0 jos ollaan tv-listalla ja 1 jos ollaan tallenne-listalla
        self.kanavalistasijainti=[0,0] #tv ja tallenne sijainnit
        self.tvklik()


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
        if self.omaProsessi is not None: #jos oma ulkoinen skripti päällä
            if nappi in ["STOP", "BACK"]: #pysäytetään oma skripti !TODO kuinka tää kuuluu oikeasti tehdä?
                debug("tapetaan oma")
                debug("A")
                killingProcess = "kill -TERM -" + str(self.omaProsessi.pid())
                os.system(killingProcess)
                time.sleep(0.1)
                debug("B")
                self.omaProsessi.close()
                debug("C")
                self.omaProsessi.kill()
                debug("D")
                self.omaProsessi.waitForFinished(1)
                debug("E")
                self.omaProsessi=None
                debug("F")
                Form.showMaximized()
                self.frame_ala.show()
                self.btn_tv.setFocus()
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
        if widget is None: #esim kun omasta skriptistä tullaan ulos, voi olla hetken tällainen tilanne
            return
        obj=widget.objectName() #aktiivisen widgetin nimi
        debug("widget",widget, obj)
        if widget == self.list_menu and nappi == "BACK":
            self.frame_raitatausta.hide()
            self.btn_tv.setFocus()
        if widget == self.list_ohjelma and self.list_ohjelma.isVisible():
            debug("list_ohjelma")
            if nappi in ["YLÖS", "ALAS", "OK"]:
                event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, nappain, QtCore.Qt.NoModifier)
                QtCore.QCoreApplication.sendEvent(widget, event)
            elif nappi in ["VASEN", "BACK"]: #piilota kanavalista
                debug("piilota kanavalista")
                self.frame_ohjelma.hide()
                self.frame_video.move(0,0)
                self.frame_video.setFixedSize(self.monitor.width(),self.monitor.height())
                self.alapalkkiShow()
        elif nappi in ["OK", "YLÖS"] and obj[:3] == "btn" and self.frame_ala.isVisible():
            widget.click()
        elif nappi in ["ALAS", "BACK"] and obj[:3] == "btn":
            self.frame_ala.hide()
        elif nappi in ["VASEN", "OIKEA"] and obj[:3] == "btn":
            event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, nappain, QtCore.Qt.NoModifier)
            QtCore.QCoreApplication.sendEvent(widget, event)
        elif nappi in ["YLÖS", "BACK"] and not self.frame_ala.isVisible():
            debug("alapalkkishow")
            self.alapalkkiShow()
        elif obj == "list_menu":
            if nappi in ["YLÖS", "ALAS", "OK"]:
                event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, nappain, QtCore.Qt.NoModifier)
                QtCore.QCoreApplication.sendEvent(widget, event)
            # elif nappi == "BACK":
            #     widget.hide()
            #     self.alapalkkiHide()

    def klikattumenu(self, tyyppi):
        if tyyppi==TRACKAUDIO:
            if self.videoPlayer is None:
                return
            self.tracks=[]
            self.list_menu.clear()
            self.list_menu.show()
            self.frame_raitatausta.show()
            for a in self.videoPlayer.audio_get_track_description():
                self.tracks.append([TRACKAUDIO,a[0]])
                self.list_menu.addItem(a[1].decode())
        elif tyyppi == TRACKTEKSTITYS:
            if self.videoPlayer is None:
                return
            self.tracks=[]
            self.list_menu.clear()
            self.list_menu.show()
            self.frame_raitatausta.show()
            for s in self.videoPlayer.video_get_spu_description():
                if [ss for ss in ["undertexter", "tekstitys", "subtitles"] if ss in s[1].decode()]:
                    self.tracks.append([TRACKTEKSTITYS,s[0]])
                    self.list_menu.addItem(s[1].decode())
        elif tyyppi == TRACKTOIMINNOT:
            self.tracks=[]
            self.list_menu.clear()
            self.list_menu.show()
            self.tracks.append([TRACKTOIMINNOT,"!stop"])
            self.list_menu.addItem("Pysäytä VLC")
            self.tracks.append([TRACKTOIMINNOT,"!reboot"])
            self.list_menu.addItem("Reboot")
            self.tracks.append([TRACKTOIMINNOT,"!halt"])
            self.list_menu.addItem("Halt")
            self.tracks.append([TRACKTOIMINNOT,"!exit"])
            self.list_menu.addItem("Poistu")
        elif tyyppi == TRACKOMA: #omia skriptejä hakemistosta ~/pycectv
            self.tracks=[]
            self.list_menu.clear()
            self.list_menu.show()
            skriptihakemisto= os.path.expanduser("~")+"/pycectv"
            if os.path.isdir(skriptihakemisto):
                filut=os.listdir(skriptihakemisto)
                for filu in filut:
                    self.tracks.append([TRACKOMA,filu])
                    self.list_menu.addItem(filu)
        self.tracks.append([-1, "!close"])
        self.list_menu.addItem("[sulje]")
        self.frame_raitatausta.show()
        self.frame_raitatausta.raise_()
        self.list_menu.show()
        self.list_menu.raise_()
        self.list_menu.setFocus()
        self.list_menu.setCurrentRow(0)

    def klikatturaita(self):
        kohde=self.list_menu.currentRow()
        debug(self.tracks[kohde],"klikattiin")
        if self.tracks[kohde][0]==TRACKAUDIO:
            self.videoPlayer.audio_set_track(self.tracks[kohde][1])
        elif self.tracks[kohde][0]==TRACKTEKSTITYS:
            self.videoPlayer.video_set_spu(self.tracks[kohde][1])
        elif self.tracks[kohde][0]==TRACKTOIMINNOT:
            if self.tracks[kohde][1] == "!stop": 
                if self.videoPlayer is not None:
                    self.stopVlc()
                    self.frame_video.update()
            elif self.tracks[kohde][1] == "!reboot":
                os.system("sudo reboot")
            elif self.tracks[kohde][1] == "!halt":
                os.system("sudo halt")
            elif self.tracks[kohde][1]=="!exit":
                if self.videoPlayer is not None:
                    self.stopVlc()
                quit()
        elif self.tracks[kohde][0]==TRACKOMA:
            if self.videoPlayer is not None:
                self.stopVlc()
            Form.hide()
            komento= "setsid -w "+os.path.expanduser("~")+"/pycectv/"+self.tracks[kohde][1]+" &"
            #self.omaProsessi = subprocess.Popen(komento, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid) 
            #debug("PID",self.omaProsessi.pid)
            self.omaProsessi=QtCore.QProcess()
            self.omaProsessi.start(komento)
        self.frame_raitatausta.hide()
        self.frame_ala.hide()


    def alapalkkiHide(self):
        #self.frame_video.setFixedSize(self.monitor.width(),self.monitor.height())
        #self.frame_video.move(0,0)
        pass
        #self.frame_ala.hide()

    def alapalkkiShow(self):
        #self.frame_video.setFixedSize(self.monitor.width(),self.monitor.height()-ALAPALKKIKORKEUS)
        #self.frame_video.move(0,0)
        self.frame_ala.show()
        self.frame_ala.raise_()
        self.btn_tv.setFocus()


    def tvklik(self):
        self.kanavalistatyyppi=0
        self.frame_video.setFixedSize(self.monitor.width()-KANAVALISTALEVEYS,self.monitor.height())
        self.frame_video.move(KANAVALISTALEVEYS,0)
        self.frame_ohjelma.show()
        self.frame_ala.hide()
        self.list_ohjelma.clear()
        self.striimiLista=[]
        self.list_ohjelma.show()
        self.list_ohjelma.setFocus()
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
        debug("kohdistetaan kanavalistalle tv kohtaan",self.kanavalistasijainti[0])
        self.list_ohjelma.setCurrentRow(self.kanavalistasijainti[0])

    def movieklik(self):
        self.kanavalistatyyppi=1
        self.frame_video.setFixedSize(self.monitor.width()-KANAVALISTALEVEYS,self.monitor.height())
        self.frame_video.move(KANAVALISTALEVEYS,0)
        self.frame_ohjelma.show()
        self.frame_ala.hide()
        self.list_ohjelma.clear()
        self.striimiLista=[]
        self.list_ohjelma.show()
        self.list_ohjelma.setFocus()
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
        debug("kohdistetaan kanavalistalle tallenne kohtaan",self.kanavalistasijainti[1])
        self.list_ohjelma.setCurrentRow(self.kanavalistasijainti[1])

    def klikattuKohde(self): #kanavalistalta klikattu ohjelmaa
        self.frame_video.move(0,0)
        self.frame_video.setFixedSize(self.monitor.width(),self.monitor.height())
        self.frame_ohjelma.hide()
        kohde=self.list_ohjelma.currentRow()
        debug("klikattukohde",kohde, self.striimiLista[kohde])
        self.list_ohjelma.hide()
        if kohde==0: #exit ekana
            return
        if self.videoPlayer is not None:
            self.stopVlc()
        soittourl=self.striimiperus+urllib.parse.quote(self.striimiLista[kohde][1])
        if self.kanavalistatyyppi==0:
            self.kanavalistasijainti[0]=kohde
            debug("kanavalista tv sijainti",self.kanavalistasijainti[0])
        elif self.kanavalistatyyppi==1:
            self.kanavalistasijainti[1]=kohde
            debug("kanavalista tallenne sijainti",self.kanavalistasijainti[1])
        debug("SOITA", soittourl)
        #self.frame_ala.hide()
        #opts=['--vbi-opaque', '--vbi-text', '--freetype-color=16776960', '--freetype-background-opacity=128', '--freetype-shadow-opacity=0', '--freetype-background-color=0', '--freetype-font=Tiresias Infofont', 
        #        '--text-renderer=any', '--freetype-rel-fontsize=-5']
        opts=['--video-on-top', '--vbi-opaque', '--vbi-text', '--freetype-color=16776960', '--freetype-background-opacity=128', '--freetype-shadow-opacity=0', '--freetype-background-color=0', '--freetype-font=Tiresias Infofont', 
               '--sub-text-scale=60', '--sub-margin=20']
        self.vlcInstance = vlc.Instance(opts)
        self.videoPlayer = self.vlcInstance.media_player_new()
        self.media = self.vlcInstance.media_new(soittourl)
        self.videoPlayer.set_media(self.media)
        self.videoPlayer.play()
        self.videoPlayer.set_xwindow(self.frame_video.winId())
        self.timerAutoraita.start()


    def autoRaidat(self): #Aseta kieli ja audio automaattisesti jos asetuksissa on suositeltuja kieliä
        debug("AUTORAITA")
        self.timerAutoraita.stop()
        akielet=config.get("alang")
        if akielet is not None:
            atracks=[]
            for a in self.videoPlayer.audio_get_track_description():
                atracks.append([a[0],a[1].decode()])
            loydetty=False
            for atoive in akielet:
                if loydetty:
                    break
                debug("etsitään aud toivetta", atoive)
                for araita in atracks:
                    debug("Akieli",araita)
                    debug("AAA",araita[1])
                    if araita[0]>0:
                        akk=araita[1].split("[")[1][:-1].lower()
                        kielikoodi= haekieli(akk)
                        debug("akielikoodi",kielikoodi)
                        if kielikoodi == atoive:
                            debug("täyttyi aud toive",kielikoodi)
                            self.videoPlayer.audio_set_track(araita[0])
                            loydetty=True
                            break

        skielet=config.get("slang")
        if skielet is not None:
            stracks=[]
            for s in self.videoPlayer.video_get_spu_description():
                if [ss for ss in ["undertexter", "tekstitys", "subtitles"] if ss in s[1].decode()]:
                    stracks.append([s[0],s[1].decode()])
            loydetty=False
            for stoive in skielet:
                if loydetty:
                    break
                debug("etsitään sub toivetta", stoive)
                for sraita in stracks:
                    skk=sraita[1].split("[")[1][:-1].lower()
                    debug(skk)
                    kielikoodi= haekieli(skk)
                    if kielikoodi == stoive:
                        debug("täyttyi sub toive",kielikoodi)
                        self.videoPlayer.video_set_spu(sraita[0])
                        loydetty=True
                        break
 
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

    def stopVlc(self):
        debug("vlc seis?")
        if self.videoPlayer is not None:
            debug("vlc seis!")
            self.videoPlayer.release()
            self.media.release()
            self.videoPlayer=None

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.showMaximized()
    sys.exit(app.exec_())
