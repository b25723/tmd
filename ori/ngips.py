import re
import hashlib
import time
import random
import string
import requests
import unittest
import sys
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


if sys.argv[1:]:
    URL='https://'+sys.argv[1]
else:
    URL='https://10.24.253.69'

IPS='/rest/profiles/ip'
AC='/rest/profiles/ac'
UF='/rest/profiles/uf'
IP='/rest/objects/ipaddrs'
IPs='/rest/objects/ipgroups'
VLAN='/rest/objects/vlans'
VLANS='/rest/objects/vlangroups'
SERV='/rest/objects/servs'
SERVS='/rest/objects/servgroups'
SCHE='/rest/objects/schds'
POL='/rest/policies/sec'

print URL
#login and get sdi
req=requests.post(URL+'/rest/admin/login',headers={'login':'rexwu','passHash':'d864934644cd577757afa824138ae169fd5ecbed','Authentication':'ZETA'},verify=False)

#a=requests.get(URL+IPS+'/3?',cookies={'sid':req.json()['sid']},verify=False)
#sig=json.loads(a.text)

a='''
{"secpolicy":{"name":"test","description":"","enabled":"Enabled","srcIpAddrs":[],"srcIpGroups":[],"dstIpAddrs":[],"dstIpGroups":[],"servs":[],"servGroups":[],"vlans":[],"vlanGroups":[],"schds":[],"action":"Allow","logging":"Disabled","ipprofile":{"id":"3"},"ipprofileLogOnly":true,"acprofile":{"id":"2"},"acprofileLogOnly":true,"ufprofile":{"id":"1"},"ufprofileLogOnly":true}}
'''

if req.status_code == 200:
    print 'login succ'
    print 'sid:{0}'.format(req.json()['sid'])
else:
    print 'login fail'

pol=json.loads(a)


def add_ips(counter=3):
    number=0

    for i in range(1,counter+1):
        sig['ipprofile']['name']='test-'+str(i)
        s=requests.post(URL+IPS,json=sig,cookies={'sid':req.json()['sid']},verify=False)
        #print s.status_code

        if s.status_code == 200:
            number+=1
            print 'create ips succ {0}'.format(number)
        else:
            print 'ips fail'
    print 'created {} profiles'.format(number)


def add_pol(counter=3):
    number=0

    for i in range(1,counter+1):
        s=requests.get(URL+POL+'?pending=true',cookies={'sid':req.json()['sid']},verify=False)
        #print s.status_code
        mtag={'MTag': str(s.headers['mtag'])}
        #print mtag
        pol['secpolicy']['name']='test-'+str(i)
        #print pol['secpolicy']['name']
        s=requests.post(URL+POL,json=pol,cookies={'sid':req.json()['sid']},headers=mtag,verify=False)
        #s=requests.put(URL+POL,json=pol,cookies={'sid':req.json()['sid']},headers=mtag,verify=False)
        #print s.status_code
        p=requests.post(URL+POL+'/pending',cookies={'sid':req.json()['sid']},verify=False)
        #print p.status_code

        if s.status_code == 200 and p.status_code == 204:
            number+=1
            print 'create pol succ {0}'.format(number)
        else:
            print 'create pol fail'

    print 'created {} policies'.format(number)


def del_ips():
    number=0

    r=requests.get(URL+IPS+'?ipprofiles=0&itemsPerPage=0',cookies={'sid':req.json()['sid']},verify=False)
    #print r.content
    d=re.findall('\"id\"\:(\d{1,4})\,\"name\"',r.content)
    #print d
    #print len(d)

    for ds in d:
        r=requests.delete(URL+IPS+'?ipprofiles={0}'.format(ds),cookies={'sid':req.json()['sid']},verify=False)
        #print r.status_code
    #print r.text
        if r.status_code == 204:
            number+=1
            print 'del succ {0}'.format(number)
        else:
            print 'del fail'
    print 'deleted {} profiles'.format(number)



def del_pol():

    r=requests.get(URL+POL+'?pending=true',cookies={'sid':req.json()['sid']},verify=False)
    mtag={'MTag': str(r.headers['mtag'])}
    r=requests.get(URL+POL+'?secpolicies=0',cookies={'sid':req.json()['sid']},verify=False)
    #print r.content
    d=re.findall('\{\"id\"\:(\d{4,6})\,\"name\"',r.content)
    total=re.search('\"total\"\:(\d{1,4})',r.content).group(1)
    #print total
    #print d

    r=requests.delete(URL+POL+'?secpolicies={0}'.format(','.join(d)),headers=mtag,cookies={'sid':req.json()['sid']},verify=False)
    p=requests.post(URL+POL+'/pending',cookies={'sid':req.json()['sid']},verify=False)
    #print r.status_code
    #print p.status_code

    if r.status_code == 204 and p.status_code == 204:
        print 'del succ'
    else:
        print 'del fail'
    print 'deleted {0} policies'.format(total)


def update_pol():
    number=0

    r=requests.get(URL+POL+'?secpolicies=0',cookies={'sid':req.json()['sid']},verify=False)
    #print r.url
    #print r.content
    #d=re.findall('\,\"name\"\:\"(\w{1,64})\"\,\"description\"',r.content)
    d=re.findall('\{\"id\"\:(\d{4,6})\,\"name\"',r.content)
    #print d

    for ds in d:
        r=requests.get(URL+POL+'?pending=true',cookies={'sid':req.json()['sid']},verify=False)
        mtag={'MTag': str(r.headers['mtag'])}
        #print mtag
        #print r.url
        pol['secpolicy']['description']=''.join(random.choice(string.printable) for i in xrange(random.randint(1,64),random.randint(128,256)))
        pol['secpolicy']['name']=''.join(random.choice(string.printable) for i in xrange(random.randint(1,32),random.randint(32,64)))
        #print pol
        #https://10.24.254.71/rest/policies/sec/1465?pending=true&_=1465996198787
        r=requests.get(URL+POL+'/{0}?pending=true'.format(ds),headers=mtag,cookies={'sid':req.json()['sid']},verify=False)
        #print r.url

        r=requests.put(URL+POL+'/{0}'.format(ds),json=pol,headers=mtag,cookies={'sid':req.json()['sid']},verify=False)
        #print r.status_code
        #print r.url
        #print r.headers

        if r.status_code == 200:
            number+=1
            print 'updated succ'
        else:
            print 'updated fail'

    p=requests.post(URL+POL+'/pending',cookies={'sid':req.json()['sid']},verify=False)
    print 'updated {0} policies'.format(number)


def retrieve():
    global d11

    s1=requests.get(URL+IP+'?',cookies={'sid':req.json()['sid']},verify=False)
    d1=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s1.content)
    s2=requests.get(URL+IPS+'?',cookies={'sid':req.json()['sid']},verify=False)
    d2=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s2.content)
    s3=requests.get(URL+UF+'?',cookies={'sid':req.json()['sid']},verify=False)
    d3=re.findall('\[\{\"id\"\:(\d{1,4})\,\"',s3.content)
    s4=requests.get(URL+AC+'?',cookies={'sid':req.json()['sid']},verify=False)
    d4=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s4.content)
    s5=requests.get(URL+IPs+'?',cookies={'sid':req.json()['sid']},verify=False)
    d5=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s5.content)
    s6=requests.get(URL+VLAN+'?',cookies={'sid':req.json()['sid']},verify=False)
    d6=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s6.content)
    s7=requests.get(URL+VLANS+'?',cookies={'sid':req.json()['sid']},verify=False)
    d7=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s7.content)
    s8=requests.get(URL+SERV+'?',cookies={'sid':req.json()['sid']},verify=False)
    d8=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s8.content)
    s9=requests.get(URL+SERVS+'?',cookies={'sid':req.json()['sid']},verify=False)
    d9=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s9.content)
    s10=requests.get(URL+SCHE+'?',cookies={'sid':req.json()['sid']},verify=False)
    d10=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s10.content)
    s11=requests.get(URL+POL+'?',cookies={'sid':req.json()['sid']},verify=False)
    d11=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s11.content)
    #d11+=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s11.content)


    return d1,d2,d3,d4,d5,d6,d7,d8,d9,d10


#rancho=lambda x:random.choice(x)

def fuzz():
    '''
    add encoding scheme for some inputing or content
    add content comparison or display -> hashlib
    add a judgement for counter
    add a judgement for expected response or using unitest to do assertion

    '{"secpolicy":{"name":"%s","description":"%s","enabled":"%s","srcIpAddrs":[],"srcIpGroups":[],"dstIpAddrs":[],"dstIpGroups":[],"servs":[],"servGroups":[],"vlans":[],"vlanGroups":[],"schds":[],"action":"%s","logging":"%s","ipprofile":{"id":"3"},"ipprofileLogOnly":%s,"acprofile":{"id":"2"},"acprofileLogOnly":%s,"ufprofile":{"id":"1"},"ufprofileLogOnly":%s}}'%(8 items)

    '''
    #pass
    try:

        #a=[[1,2,3,4],[5,6,7,8],[9,10,11],[12,13,14],[15,16],[17,18,19],[20,21,22],[23,24]]
        #a=retrieve()
        a=[['test1','test2'],['test1-desc','test2-desc'],['Enable','Disable'],['allow','deny'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false'],['true','false']]
        #print [random.choice(a[i])for i in range(8)]
        b,c,d,e,f,g,h,i,j,k,l,h,m,p,q,r,s,t,u,v=[random.choice(a[i])for i in range(20)]
        print len(a)
        #(lambda x:[[random.choice(a[i])for i in range(8)].pop(x)])(4)
        f1=lambda x:[[random.choice(a[i])for i in range(8)].pop(x)]
        print '{"secpolicy":{"name":"%s","description":"%s","enabled":"%s","srcIpAddrs":[{"id":"%s"}],"srcIpGroups":[{"id":"%s"}],"dstIpAddrs":[{"id":"%s"}],"dstIpGroups":[{"id":"%s"}],"servs":[{"id":"%s"}],"servGroups":[{"id":"%s"}],"vlans":[{"id":"%s"}],"vlanGroups":[{"id":"%s"}],"schds":[{"id":"%s"}],"action":"%s","logging":"%s","ipprofile":{"id":"%s"},"ipprofileLogOnly":%s,"acprofile":{"id":"%s"},"acprofileLogOnly":%s,"ufprofile":{"id":"%s"},"ufprofileLogOnly":%s}}' % (b,c,d,e,f,g,h,i,j,k,l,h,m,p,q,r,s,t,u,v)
        #20 items

    #except Exception,e:
    except Exception as e:
        print e
        #raise 'error' #TypeError()
        #pass

    finally:
        print 'here'



def get_nodes():

    s=requests.get(URL+'/rest/nodes',cookies={'sid':req.json()['sid']},verify=False)
    print s.status_code
    print s.content
    return s.content


#b='{"node":{"instanceId":"69471f76-57ed-466b-8521-94faf5a0c03c","name":"test001","type":"ips","ip":"192.168.1.26","description":"test purpose"}}'
#b='{"node":{"instanceId":"95f7161a-0a1b-461c-a255-49fcfbaf280b","name":"nested","type":"VNFS","ip":"10.24.254.207","description":"vnfs"}}'
#b='{"node":{"instanceId":"95f7161a-0a1b-461c-a255-49fcfbaf280b","name":"hardware","type":"VNFS","ip":"","description":"virt-vnfs"}}'
b='{"node":{"instanceId":"62ca81a4-dc1f-40b7-8d73-38dea4c9beb0","name":"BVT_generic3","type":"F07","ip":"","description":"virt-vnfs"}}'
#b='{"node":{"instanceId":"deadbeef-dead-beef-dead-beefdeadbee0","name":"BVT_generic0","type":"F07","ip":"","description":"virt-vnfs"}}'
nodet=json.loads(b)

def add_node():

    s=requests.post(URL+'/rest/nodes',json=nodet,cookies={'sid':req.json()['sid']},verify=False)
    #s=requests.delete(URL+'/rest/nodes?nodes=1',cookies={'sid':req.json()['sid']},verify=False)
    print s.status_code
    print s.content
    #print nodet['node']


def del_node():
    #s=requests.delete(URL+'/rest/nodes?nodes=1',cookies={'sid':req.json()['sid']},verify=False)
    s=requests.delete(URL+'/rest/nodes/1',cookies={'sid':req.json()['sid']},verify=False)
    print s.status_code
    print s.content
    #print nodet['node']





#=====================================================================

#add_ips(1)
#del_ips()
#add_pol(1020)
#update_pol()
#del_pol()

#retrieve()
#a=retrieve()
#print d11
#fuzz()
#add_node()
#del_node()
get_nodes()
