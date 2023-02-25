import requests
import base64
from lxml import etree
import time


search_data='"redis" && port="6379" && country="CN"'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38',
    'cookie': 'fofa_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MTI4MDA4LCJtaWQiOjEwMDA3NjE2NywidXNlcm5hbWUiOiJIQUlSVUlfSCIsImV4cCI6MTY0OTcwNzE2Nn0.JpEFI2SJjFpJPBG3K_X1Jve3MNFc8Bgj6Ukj3UztB1yCoyhfPkUbvWuIcouJpZ1Rm1M1X3CiLNB8VLOwIIAiRg; user={"id":128008,"mid":100076167,"is_admin":false,"username":"HAIRUI_H","nickname":"HAIRUI_H","email":"1723433302@qq.com"; refresh_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MTI4MDA4LCJtaWQiOjEwMDA3NjE2NywidXNlcm5hbWUiOiJIQUlSVUlfSCIsImV4cCI6MTY0OTkyMzE2NiwiaXNzIjoicmVmcmVzaCJ9.bJ86U8NLeMeMkC0C0E2srsf8iZujjoSjid5Q2tMz_2vZq__4dV_zgsDDbt2ypoxYrWwGbOz7TUYyL52s4fVRgA;'
}
for page in range(1,6):
    url='https://fofa.info/result?&qbase64='
    search_data_base64=str(base64.b64encode(search_data.encode('utf-8')),'utf-8')
    # print(search_data_base64)
    urls=url+search_data_base64+'&page='+str(page)+'&page_size=10'
    try:
        # print(urls)
        result=requests.get(urls,headers=headers).content.decode('utf-8')
        # print(result)
        soup=etree.HTML(result)
        # ip_data=soup.xpath('/html/body/div/div/div/div/div/div/div/div/div/div/div/span/a/@href')
        ip_data=soup.xpath('/html/body/div/div/div/div/div/div/div/div/div/div/div/span/text()')
        print(ip_data)
        ipdata='\n'.join(ip_data)
        with open('D:\\BaiduNetdiskDownload\\笔记\\安全\\安全编程\\redis_ip.txt','a+') as f:
            f.write(ipdata+'\n')
            f.close
    except Exception as e:
        pass
    time.sleep(2)