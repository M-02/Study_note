import requests
import json
import time

def sqlmap_api(url):
    data={
        'url':url,
        'data':'keyword=1'
    }
    headers={
        'Content-Type':'application/json'
    }
    # 创建任务ID
    task_new_url='http://127.0.0.1:8775/task/new'
    resp=requests.get(task_new_url)
    task_id=resp.json()['taskid']
    # print(resp.json())
    if 'success' in resp.content.decode("utf-8"):
        print('SQLMap Created new task success')
        # 设置任务ID的配置信息（扫描信息）
        task_set_url='http://127.0.0.1:8775/option/'+task_id+'/set'
        task_set_resp=requests.post(task_set_url,data=json.dumps(data),headers=headers)
        # print(task_set_resp.json())
        print('SQLMap set task success')
        if 'success' in task_set_resp.content.decode("utf-8"):
            # 启动对应ID的扫描任务
            task_start_url='http://127.0.0.1:8775/scan/'+task_id+'/start'
            task_start_resp=requests.post(task_start_url,data=json.dumps(data),headers=headers)
            # print(task_start_resp.json())
            print('SQLMap start task success')
            if 'success' in task_start_resp.content.decode("utf-8"):
                 while(1):
                # 获取扫描状态
                    task_status_url='http://127.0.0.1:8775/scan/'+task_id+'/status'
                    task_status_resp=requests.get(task_status_url)
                    # print(task_status_resp.json())
                    # print('SQLMap scan running')
                    if 'running' in task_status_resp.content.decode("utf-8"):
                        print('sqlmap scan '+url+' running please wait')
                        pass
                    else:
                    # 获取扫描结果
                        task_data_url='http://127.0.0.1:8775/scan/'+task_id+'/data'
                        task_data_resp=requests.get(task_data_url)
                        scandata=task_data_resp.content.decode("utf-8")
                        print(scandata)
                        with open(r'scan_result.txt','a+') as f:
                            f.write(url+'\n')
                            f.write(scandata+'\n')
                            f.write('====================================='+'\n')
                            f.close
                        task_del_url='http://127.0.0.1:8775/task/'+task_id+'/delete'
                        task_del_resp=requests.get(task_del_url)
                        if 'success' in task_del_resp.content.decode('utf-8'):
                            print('SQLMap delete task success')
                        break
                    time.sleep(3)
                 

if __name__=='__main__':
    for url in open('url.txt'):
        url=url.replace('\n','')
        sqlmap_api(url)
