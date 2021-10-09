#!/usr/bin/python
import sys
import nmap

host=sys.argv[1]
port=sys.argv[2]
# host = input('Enter host:')
# print('\n')
# port = input('Enter port:')
print('*'*50)
nmScan = nmap.PortScanner()
print(nmScan.scan(host, port), '\n', '*'*50)
print(nmScan.command_line)
for host in nmScan.all_hosts():
    print('Host: %s (%s)' % (host, nmScan[host].hostname()))
    print('State%s' % nmScan[host] .state())
    for proto in nmScan[host].all_protocols():
        print('Protocol : %s' % proto)
        lport = nmScan[host][proto].keys()
        sorted(lport)
        for port in lport:
            print('port : %s\tstate : %s' %
                  (port, nmScan[host][proto][port]['state']))
