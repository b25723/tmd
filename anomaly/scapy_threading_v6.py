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

#logging.basicConfig(filename='./example.log',filemode='w',level=logging.DEBUG)
#logging.debug('test for debug file')

if len(sys.argv)-1 != 5:
	print 'error,at least, 5 parameters must included'
	print '{0} pkts iteration srcinf dstinf wait'.format(sys.argv[0])
	sys.exit()

srchost='1.1.1.1'
dsthost='1.1.1.2'
brdhost='1.1.1.255'
inf=sys.argv[3]
nic=str(sys.argv[4])
#pkts=100
pkts=int(sys.argv[1])

anomaly= [
[["udp_flood"],["sendpfast(Ether()/IP(src='{0}',dst='{1}')/UDP(sport=(100,{3}),dport=100),iface='{2}')".format(srchost,dsthost,inf,pkts)]],
[["tcp_port_scan"],["sendpfast(Ether()/IP(src='{0}',dst='{1}')/TCP(flags='S',dport=(100,{3})),iface='{2}')".format(srchost,dsthost,inf,100+pkts)]],
[["udp_port_scan"],["sendpfast(Ether()/IP(src='{0}',dst='{1}')/UDP(sport=(100,{3}),dport=100),iface='{2}')".format(srchost,dsthost,inf,100+pkts)]],
[["ip_sweep"],["sendpfast(Ether()/IP(src='{0}',dst='{1}/27'),iface='{2}')".format(srchost,dsthost,inf)]],
[["tcp_null_scan"],["sendpfast(Ether()/IP(src='{0}',dst='{1}')/TCP(dport=(1,{3}),flags='',window=1024),iface='{2}')".format(srchost,dsthost,inf,1+pkts)]],
[["tcp_port_syn_scan\\flood"],["sendpfast(Ether()/IP(src='{0}',dst='{1}')/TCP(flags='S',seq=1,dport=(100,{3})),iface='{2}')".format(srchost,dsthost,inf,100+pkts)]],
[["tcp_port_xmas_scan"],["sendpfast(Ether()/IP(src='{0}',dst='{1}')/TCP(flags='PFU',seq=1,dport=(100,{3})),iface='{2}')".format(srchost,dsthost,inf,100+pkts)]],
[["tcp_syn_flood"],["sendpfast(Ether()/IP(src='{0}',dst='{1}')/TCP(sport=(1,{3}),dport=80),iface='{2}')".format(srchost,dsthost,inf,1+pkts)]],
[["icmp_flood"],["sendpfast(Ether()/IP(src='{0}',dst='{1}',id=(1,{3}))/ICMP(),iface='{2}')".format(srchost,dsthost,inf,pkts)]],
[["tcp_port_fin scan"],["sendpfast(Ether()/IP(src='{0}',dst='{1}')/TCP(flags='F',seq=1,dport=(100,{3})),iface='{2}')".format(srchost,dsthost,inf,100+pkts)]],
[["igmp_flood"],["sendpfast(Ether()/IP(src='{0}',dst='{1}',id=(1,{3}))/IGMP(),iface='{2}')".format(srchost,dsthost,inf,pkts)]],
[["ip_fragment_timeout"],["sendp(fragment(Ether()/IP(src='{0}',dst='{1}')/('a'*4096),1024),iface='{2}')".format(srchost,dsthost,inf)]],
[["tcp_land"],["sendp(Ether()/IP(src='{0}',dst='{1}')/TCP(dport=10,sport=10),iface='{2}')".format(srchost,srchost,inf)]],
[["ip_fragment_attack"],["sendp(fragment(Ether()/IP(src='{0}',dst='{1}',frag=2)/('a'*32),1),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_bad_flag_uf"],["sendp(Ether()/IP(src='{0}',dst='{1}',flags=4,frag=0)/TCP(sport=1500,dport=80,flags='S',seq=4096),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_bad_df_mf"],["sendp(Ether()/IP(src='{0}',dst='{1}',flags=3,frag=0)/TCP(sport=1500,dport=80,flags='S'),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_truncated"],["sendp(Ether()/IP(src='{0}',dst='{1}',len=9000),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_bad_version"],["sendp(Ether()/IP(src='{0}',dst='{1}',version=0),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_bad_length"],["sendp(Ether()/IP(src='{0}',dst='{1}',len=1),iface='{2}')".format(srchost,dsthost,inf)]],
[["igmp_bad"],["sendp(Ether()/IP(src='{0}',dst='{1}')/IGMP(type=0),iface='{2}')".format(srchost,dsthost,inf)]],
[["tcp_broadcast"],["sendp(Ether()/IP(src='{0}',dst='{1}')/TCP(),iface='{2}')".format(srchost,brdhost,inf)]],
[["udp_smurf"],["sendp(Ether()/IP(src='{0}',dst='{1}')/UDP(),iface='{2}')".format(srchost,brdhost,inf)]],
[["icmp_smurf"],["sendp(Ether()/IP(src='{0}',dst='{1}')/ICMP(),iface='{2}')".format(srchost,brdhost,inf)]],
[["bad_tcp_checksum"],["sendp(Ether()/IP(src='{0}',dst='{1}')/TCP(chksum=0),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_flood_truncated"],["sendp(Ether()/IP(src='{0}',dst='{1}',len=65535)/TCP(sport=(1,2),flags='F',window=1024,seq=0),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_fragment_oversize"],["sendp(fragment(Ether()/IP(src='{0}',dst='{1}')/ICMP()/('a'*9000),),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_bad_udp_l4_size"],["sendp(Ether()/IP(src='{0}',dst='{1}')/UDP(len=90)*1,iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_bad_tcp_l4_size"],["sendp(Ether()/IP(src='{0}',dst='{1}',len=30)/TCP(flags='P'),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_bad_igmp_l4_size"],["sendp(Ether()/IP(src='{0}',dst='{1}',len=22)/IGMP(mrtime=100),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_bad_icmp_l4_size"],["sendp(Ether()/IP(src='{0}',dst='{1}',len=23)/ICMP(),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_bad_ip_option"],["sendp(Ether()/IP(src='{0}',dst='{1}',proto=255,options=IPOption('a'*10)),iface='{2}')".format(srchost,dsthost,inf)]],
[["ip_spoofing"],["sendp(Ether()/IP(src='{0}',dst='{1}')/ICMP(),iface='{2}')".format(srchost,dsthost,inf)]],
[["bad_tcp_option"],["sendp(Ether()/IP(src='{0}',dst='{1}')/TCP(flags=[46],dataofs=[46])/('a'*1000),iface='{2}')".format(srchost,dsthost,inf)]],
[["udp_land"],["sendp(Ether()/IP(src='{0}',dst='{1}')/UDP(),iface='{2}')".format(srchost,srchost,inf)]],
[["ip_fragment_teardrop"],["sendp(Ether()/IP(src='{0}',dst='{1}',flags=[0,1],frag=46)/('a'*1000),iface='{2}')".format(srchost,dsthost,inf)]],
[["bad_tcp_checksum"],["sendp(Ether()/IP(src='{0}',dst='{1}')/TCP(chksum=0),iface='{2}')".format(srchost,dsthost,inf)]],

]

'''
temp=[
]
'''


z=0
res=[0,0]

def snf(r,item):
	s=sniff(iface=nic,timeout=2,count=pkts)
	#s=sniff(iface=nic,timeout=1)
	#s.summary()
	#print s
	#print pkts
	#print anomaly
	#print anomaly[item][1]
	type=''.join(anomaly[item][0])
	#print type
	if len(s) > 0:
		#wrpcap('/tmp/{0}.pcap'.format(r[0]+r[1]),s)
		wrpcap('/tmp/{0}.pcap'.format(type),s)
		#print '\n'
		#print 'recevied pkts={0}'.format(len(s))
		try:
			if 'count' in anomaly[item][1]:
				if len(s) == pkts:
					#print 'result=pass\n'
					r[0]+=1
					#print r[0]
				else:
					#print 'result=fail\n'
					r[1]+=1
					#print r[1]
			else:
				if len(s) > 0:
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
		t1=threading.Thread(target=snf,args=(res,i))
		t1.start()
		t2=threading.Thread(target=ply,args=(anomaly,i))
		t2.start()
		t2.join()
		#print 'finished'
		time.sleep(float(sys.argv[5]))
	time.sleep(2)
	logging.info('pass:{0} fail:{1}'.format(res[0],res[1]))
	logging.info('total:{0}'.format(res[0]+res[1]))
	print 'pass:{0} fail:{1}'.format(res[0],res[1])
	print 'total case {0}'.format(len(anomaly))
	logging.info(time.time() - begin)

for i in range(int(sys.argv[2])):
	main()

#logging.info('total run:{0}'.format(z))

#coding:utf8
a=[1,2,3,4,5]
b='''string is me'''

#global pktcount
pktcount=800

