#coding:utf8
import threading
from scapy.all import *
import time
import sys
import logging
from scapy.contrib.igmp import IGMP
#load_contrib('igmp')
#import config
#import warnings
#warnings.simplefilter("ignore", Warning)

#conf.iface='eth0'
conf.verb=0

if len(sys.argv)-1 != 6:
    print 'error,at least, 6 parameters must included'
    print 'usage: {0} pkts iteration srcinf dstinf wait gwmac'.format(sys.argv[0])
    sys.exit()


#logging.basicConfig(filename='./example.log',filemode='w',level=logging.DEBUG)
#logging.debug('test for debug file')

srchost='1.1.1.1'
dsthost='1.1.1.2'
brdhost='1.1.1.255'
inf=sys.argv[3]
nic=str(sys.argv[4])
gwmac=str(sys.argv[6])
#pkts=100
pkts=int(sys.argv[1])

anomaly= [
[["tcp_land"],["sendp(Ether(dst='{4}')/IP(src='{0}',dst='{1}')/TCP(dport=10,sport=10),iface='{2}',count={3})".format(srchost,srchost,inf,pkts,gwmac)]],
[["tcp_syn_flood"],["sendp(Ether(dst='{4}')/IP(src='{0}',dst='{1}')/TCP(sport=(1,{3}),dport=80),iface='{2}')".format(srchost,dsthost,inf,pkts,gwmac)]],
[["icmp flood"],["sendp(Ether(dst='{4}')/IP(src='{0}',dst='{1}')/ICMP(),iface='{2}',count={3})".format(srchost,dsthost,inf,pkts,gwmac)]],
[["igmp flood"],["sendp(Ether(dst='{4}')/IP(src='{0}',dst='{1}')/IGMP(),iface='{2}',count={3})".format(srchost,dsthost,inf,pkts,gwmac)]],
[["ip fragment timeout"],["sendp(fragment(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/('a'*4096),1024),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip fragment attack"],["sendp(fragment(Ether(dst='{3}')/IP(src='{0}',dst='{1}',frag=2)/('a'*32),1),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip bad flag uf"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',flags=4,frag=0)/TCP(sport=1500,dport=80,flags='S',seq=4096),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip bad df mf"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',flags=3,frag=0)/TCP(sport=1500,dport=80,flags='S'),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip truncated"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',len=9000),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip bad version"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',version=0),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip bad length"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',len=1),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["igmp bad"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/IGMP(type=0),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["tcp broadcast"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/TCP(),iface='{2}')".format(srchost,brdhost,inf,gwmac)]],
[["udp smurf"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/UDP(),iface='{2}')".format(srchost,brdhost,inf,gwmac)]],
[["icmp smurf"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/ICMP(),iface='{2}')".format(srchost,brdhost,inf,gwmac)]],
[["bad tcp checksum"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/TCP(chksum=0),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip sweep"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}/30')/TCP(),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["tcp null scan"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/TCP(sport=(1,2),flags='',window=1024),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip flood truncated"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',len=65535)/TCP(sport=(1,2),flags='F',window=1024,seq=0),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["udp flood"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',ttl=(1,5))/UDP(),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["tcp port syn scan/flood"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/TCP(flags='S',seq=1,dport=(100,110)),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["udp port scan"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/UDP(dport=(100,105)),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["tcp port xmas scan"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/TCP(flags='FPU',seq=1,dport=(101,105)),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip fragment oversize"],["sendp(fragment(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/ICMP()/('a'*9000),),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip bad udp l4 size"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/UDP(len=90)*1,iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip bad tcp l4 size"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',len=30)/TCP(flags='P'),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip bad igmp l4 size"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',len=22)/IGMP(mrtime=100),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip bad icmp l4 size"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',len=23)/ICMP(),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip bad ip option"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',proto=255,options=IPOption('a'*10)),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["tcp port scan"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/TCP(flags='F',dport=(100,500)),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip_spoofing"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/ICMP(),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["bad tcp option"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/TCP(flags=[46],dataofs=[46])/('a'*1000),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["tcp port fin scan"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/TCP(flags='F',seq=1,dport=(100,102)),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["udp land"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/UDP(),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["ip fragment teardrop"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}',flags=[0,1],frag=46)/('a'*1000),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],
[["bad_tcp_checksum"],["sendp(Ether(dst='{3}')/IP(src='{0}',dst='{1}')/TCP(chksum=0),iface='{2}')".format(srchost,dsthost,inf,gwmac)]],

]

'''
temp=[
] 
'''


z=0
res=[0,0]

def snf(r):
	s=sniff(iface=nic,timeout=1)
	#s.summary()
	wrpcap('/tmp/{0}.pcap'.format(r[0]+r[1]),s)
	#print '\n'
	#print 'recevied pkts={0}'.format(len(s))
	try:
		if len(s) == pkts:
			#print 'result=pass\n'
			r[0]+=1
			#print r[0]
		else:
			#print 'result=fail\n'
			r[1]+=1
			#print r[1]
	except Exception as e:
		print e

def ply(anomaly,item):
	pkt=''.join(anomaly[item][1])
	#print anomaly[item][0],
	#print pkt
	print "{0} => {1}".format(anomaly[item][0],pkt)
	#exec anomaly[0][1]
	exec pkt
	#print 'packet sent'

def main():
	begin=time.time()
	a=len(anomaly)
	for i in range(a):
		#print anomaly[i][0]
		#t1=threading.Thread(target=snf,args=(res,'src host {0} and dst host {1}'.format(srchost,dsthost)))
		t1=threading.Thread(target=snf,args=(res,))
		t1.start()
		t2=threading.Thread(target=ply,args=(anomaly,i))
		t2.start()
		t2.join()
		#print 'finished'
		time.sleep(float(sys.argv[5]))
	#time.sleep(int(sys.argv[5]))
	logging.info('pass:{0} fail:{1}'.format(res[0],res[1]))
	logging.info('total:{0}'.format(res[0]+res[1]))
	print 'pass:{0} fail:{1}'.format(res[0],res[1])
	logging.info(time.time() - begin)

for i in range(int(sys.argv[2])):
	main()

#logging.info('total run:{0}'.format(z))

#coding:utf8
a=[1,2,3,4,5]
b='''string is me'''

#global pktcount
pktcount=800

