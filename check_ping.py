#!/usr/bin/env python
# coding:utf-8
import multiprocessing
import re
import sys, os
import commands
import datetime

# compact Mac and linux
def pinger(ip):
    cmd = 'ping -c 2 %s' % (ip.strip())
    ret = commands.getoutput(cmd)
    print ret
    loss_re = re.compile(r"received, (.*) packet loss")
    packet_loss = loss_re.findall(ret)[0]
    rtt_re = re.compile(r"min/avg/max/.*? = (.*?) ",re.S)
    rtts = rtt_re.findall(ret)
    # rtt.split(["/"])
    print rtts
    rtt = rtts[0].split('/')
    rtt_min = rtt[0]
    rtt_avg = rtt[1]
    rtt_max = rtt[2]
    print "%s\t\t%s\t\t%s\t\t%s\t\t%s" % (ip, packet_loss, rtt_min, rtt_max, rtt_avg)


if __name__ == "__main__":
    if not os.path.exists("hosts.txt"):
        print u"\033[31mhosts.txt文件不存在，请重试\033[0m"
        sys.exit(1)
    now = datetime.datetime.now()
    file = open('hosts.txt', 'r')
    pool = multiprocessing.Pool(processes=4)
    result = []
    print "########%s###########" % now
    print "IPADDRSS\t\t\tLOSS\t\tMIN\t\tMAX\t\tAVG"
    for i in file.readlines():
        # print i
        if len(i) == 1 or i.startswith("#"):
            print 'In if case:'
            continue
        result.append(pool.apply_async(pinger, (i.strip(),)))
    pool.close()
    pool.join()
