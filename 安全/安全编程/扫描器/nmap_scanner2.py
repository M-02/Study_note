#!/usr/bin/python3

import nmap
import optparse


def nmapScan(inhost, inport):
    nmscan = nmap.PortSacnner()
    nmscan.scan(inhost, inport)
    state = nmscan[inhost]['tcp'][int(inport)]['state']
    print(" [*] “+ inhost + tcp/"+inport + " "+state)


def main():
    parser = optparse.OptionParser(
        'Script Usage: '+'-H <target host> -P <target port>')
    parser.add_option('-H', dest='inhost', type='string',
                      help='specify target host')
    parser.add_option('-P', dest='inport', type='string',
                      help='specify target port[s] separated by comr')

    (options, args) = parser.parse_args()
    inhost = options.inhost
    inports = str(options.inport)

    if (inhost == None) | (inports[0] == None):
        print(parser.usage)
        exit(0)

    ports = inports.strip("'").split(',')
    for inport in ports:
        nmapScan(inhost, inport)


if __name__ == '__main__':
    main()
