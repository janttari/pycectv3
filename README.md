# pycectv3

Enigma2 toistaja Raspberrylle.  
Tällä ohjelmalla ja Raspberryllä voit katsella Enigma2-boksilta suoria lähetyksiä ja tallenteita.  
Ohjelman ohjaus tapahtuu TV:n kaukosäätimen kautta (HDMI-CEC)  

![](https://raw.githubusercontent.com/janttari/pycectv3/main/doc/kuvat/demo.png)
  
Säädä tiedosto ~/.config/pycectv.conf  
  
    enigmaurl=http://192.168.1.12  
    user=root  
    pass=XXXX
    alang=fin,swe,eng
    slang=dut,fin,swe
 
 enigmaurl | enigma2-boksi osoite  
 user | käyttäjänimi jolla kirjaudutaan enigma2-boksille  
 pass | enigma2-boksin salasana  
 alang | automaattisten audio-kielien valinta tärkeysjärjestyksessä pilkulla erotettuna  
 slang | automaattiseten tekstitys-kielien valinta tärkeysjärjestyksessä pilkulla erotettuna  
 
      
Riippuvuudet:  
  
    sudo apt update &&sudo apt upgrade -y
    sudo apt install -y python3-pip python3-pyqt5 vlc cec-utils unclutter
    sudo pip3 install cec python-vlc configobj

    
Kun riippuvuudet on asennettu ja konfiguraatiotiedosto säädetty kuntoon,  
tiedosto https://github.com/janttari/pycectv3/blob/main/raspberry/pycectv3.py  
on ainoa tarvittava, joten sen voi ladata suoraankin.  
  
Jos haluaa teksti-tv-tekstitystä varten hyvän fontin, sen voi ladata: https://www.fontsquirrel.com/fonts/tiresias-infofont  
  
-----
    
Todo:  
  
- [x] ok painike toimii nyt alapalkin ollessa piilossa vaikkei pitäisi 
- [x] suosituille kielille valinta (audio ja tekstitys)
- [x] omat skriptit valikkoon TV ja Tallennne lisäksi
- [x] tallenteiden kelaus (Pause toggle toimii, eteenpäin pikakelaus 8x nopeudella, paluu 1x playlla. REV on nyt vain 1% hyppy taaksepäin. !KESKEN)
- [ ] vikasietoisuus, nyt kaatuu esim jos käynnistettäessä verkko ei ole vielä saatavilla.  
- [x] sulje-painikkeelle valikko. Tällä hetkellä se vain pysäyttää VLC-instanssin.
- [x] muista sijainti kanavalistalla uudelleen lista avattaessa
- [ ] Radio  


-----
Omia skriptejä voi laittaa hakemistoon ~/pycectv
skripti voi olla tavallinen bash-skripti, esim:
  
    #!/bin/bash
    xmessage "eka"
(tietysti chmod a+x sille että suorituskelpoinen)  
omasta skriptistä pääsee pois STOP tai BACK -näppäimellä.  
  
  
  
