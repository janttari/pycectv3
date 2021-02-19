# pycectv3

Enigma2 toistaja Raspberrylle.  
  
Säädä tiedosto ~/.config/pycectv.conf  
  
    enigmaurl=http://192.168.1.12  
    user=root  
    pass=XXXX  
      
      
Riippuvuudet:  
  
    sudo apt purge -y  piwiz 
    sudo apt update &&sudo apt upgrade -y
    sudo apt install -y python3-pip python3-pyqt5 vlc cec-utils unclutter
    sudo pip3 install cec python-vlc configobj
    
    
Todo:
-ok painike toimii nyt alapalkin ollessa piilossa vaikkei pitäisi
-suosituille kielille valinta (audio ja tekstitys)
-omat skriptit valikkoon TV ja Tallennne lisäksi
