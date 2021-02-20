# pycectv3

Enigma2 toistaja Raspberrylle.  
  
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
    
    
Todo:  
-ok painike toimii nyt alapalkin ollessa piilossa vaikkei pitäisi  
-suosituille kielille valinta (audio ja tekstitys)  
-omat skriptit valikkoon TV ja Tallennne lisäksi  
-tallenteiden kelaus  

  
