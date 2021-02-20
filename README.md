# pycectv3

Enigma2 toistaja Raspberrylle.  
Tällä ohjelmalla ja Raspberryllä voit katsella Enigma2-boksilta suoria lähetyksiä ja tallenteita.  
Ohjelman ohjaus tapahtuu TV:n kaukosäätimen kautta (HDMI-CEC)  

  
Säädä tiedosto ~/.config/pycectv.conf  
  
    enigmaurl=http://192.168.1.12  
    user=root  
    pass=XXXX  
      
      
Riippuvuudet:  
  
    sudo apt update &&sudo apt upgrade -y
    sudo apt install -y python3-pip python3-pyqt5 vlc cec-utils unclutter
    sudo pip3 install cec python-vlc configobj

    
Kun riippuvuudet on asennettu ja konfiguraatiotiedosto säädetty kuntoon,  
tiedosto https://github.com/janttari/pycectv3/blob/main/raspberry/pycectv3.py  
on ainoa tarvittava, joten sen voi ladata suoraankin.  
  
Jos haluaa teksti-tv-tekstitystä varten hyvän fontin, sen voi ladata: https://www.fontsquirrel.com/fonts/tiresias-infofont  
  
    
Todo:  
  
- [x] ok painike toimii nyt alapalkin ollessa piilossa vaikkei pitäisi 
- [ ] suosituille kielille valinta (audio ja tekstitys)
- [ ] omat skriptit valikkoon TV ja Tallennne lisäksi
- [ ] tallenteiden kelaus 
- [ ] vikasietoisuus, nyt kaatuu esim jos käynnistettäessä verkko ei ole vielä saatavilla.  
