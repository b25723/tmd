import re
import glob
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

IPS='/rest/profile/ip'
ADP='/rest/profile/ad'
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
req=requests.post(URL+'/rest/admin/login',headers={'login':'admin','passHash':'d864934644cd577757afa824138ae169fd5ecbed','Authentication':'ZETA'},verify=False)

#a=requests.get(URL+IPS+'/packages',headers={'sid':req.json()['sid']},verify=False)
#a=requests.get(URL+IPS+'/1',headers={'sid':req.json()['sid']},verify=False)
#print a
#sig=json.loads(a.text)
#print sig

#a='''
#{"secpolicy":{"name":"test","description":"","enabled":"Enabled","srcIpAddrs":[],"srcIpGroups":[],"dstIpAddrs":[],"dstIpGroups":[],"servs":[],"servGroups":[],"vlans":[],"vlanGroups":[],"schds":[],"action":"Allow","logging":"Disabled","ipprofile":{"id":"3"},"ipprofileLogOnly":true,"acprofile":{"id":"2"},"acprofileLogOnly":true,"ufprofile":{"id":"1"},"ufprofileLogOnly":true}}
#'''

if req.status_code == 200:
    print 'login succ'
    print 'sid:{0}'.format(req.json()['sid'])
else:
    print 'login fail'

#pol=json.loads(a.text)


def add_ips(counter=3):
    if glob.glob('/tmp/sig.json'):
        sig=json.loads(open('/tmp/sig.json').read())
    else:
        a=requests.get(URL+IPS+'/1',headers={'sid':req.json()['sid']},verify=False)
        with file('/tmp/sig.json','w') as f:
            f.write(a.content)
        sig=json.loads(a.text)
    number=0

    for i in range(1,counter+1):
        sig['ipProfile']['name']='test-'+str(i)
        sig['ipProfile']['enabled']=True
        s=requests.post(URL+IPS,json=sig,headers={'sid':req.json()['sid']},verify=False)
        print s.status_code

        if s.status_code == 200:
            number+=1
            print 'create ips succ {0}'.format(number)
        else:
            print 'ips fail'
    print 'created {} profiles'.format(number)

def copy_ips(counter=3):
    number=0

    for i in range(1,counter+1):
        s=requests.post(URL+IPS+'/1/duplicate',headers={'sid':req.json()['sid']},verify=False)
        print s.status_code

        if s.status_code == 200:
            number+=1
            print 'create ips succ {0}'.format(number)
        else:
            print 'ips fail'
    print 'created {} profiles'.format(number)

def add_pol(counter=3):
    number=0

    for i in range(1,counter+1):
        s=requests.get(URL+POL+'?pending=true',headers={'sid':req.json()['sid']},verify=False)
        #print s.status_code
        mtag={'MTag': str(s.headers['mtag'])}
        #print mtag
        pol['secpolicy']['name']='test-'+str(i)
        #print pol['secpolicy']['name']
        s=requests.post(URL+POL,json=pol, headers={'sid': req.json()['sid'], 'MTag': str(s.headers['mtag'])},verify=False)
        #s=requests.put(URL+POL,json=pol,headers={'sid':req.json()['sid']},headers=mtag,verify=False)
        #print s.status_code
        p=requests.post(URL+POL+'/pending',headers={'sid':req.json()['sid']},verify=False)
        #print p.status_code

        if s.status_code == 200 and p.status_code == 204:
            number+=1
            print 'create pol succ {0}'.format(number)
        else:
            print 'create pol fail'

    print 'created {} policies'.format(number)


def del_ips():
    number=0

    r=requests.get(URL+IPS+'?ipprofiles=0&itemsPerPage=0',headers={'sid':req.json()['sid']},verify=False)
    #print r.content
    d=re.findall('\"id\"\:(\d{1,4})\,\"name\"',r.content)
    #print d
    #print len(d)

    for ds in d:
        r=requests.delete(URL+IPS+'?ipprofiles={0}'.format(ds),headers={'sid':req.json()['sid']},verify=False)
        #print r.status_code
    #print r.text
        if r.status_code == 204:
            number+=1
            print 'del succ {0}'.format(number)
        else:
            print 'del fail'
    print 'deleted {} profiles'.format(number)



def del_pol():

    r=requests.get(URL+POL+'?pending=true',headers={'sid':req.json()['sid']},verify=False)
    mtag={'MTag': str(r.headers['mtag'])}
    r=requests.get(URL+POL+'?secpolicies=0',headers={'sid':req.json()['sid']},verify=False)
    #print r.content
    d=re.findall('\{\"id\"\:(\d{4,6})\,\"name\"',r.content)
    total=re.search('\"total\"\:(\d{1,4})',r.content).group(1)
    #print total
    #print d

    r=requests.delete(URL+POL+'?secpolicies={0}'.format(','.join(d)),headers={'sid':req.json()['sid'],'MTag': str(r.headers['mtag'])},verify=False)
    p=requests.post(URL+POL+'/pending',headers={'sid':req.json()['sid']},verify=False)
    #print r.status_code
    #print p.status_code

    if r.status_code == 204 and p.status_code == 204:
        print 'del succ'
    else:
        print 'del fail'
    print 'deleted {0} policies'.format(total)


def update_pol():
    number=0

    r=requests.get(URL+POL+'?secpolicies=0',headers={'sid':req.json()['sid']},verify=False)
    #print r.url
    #print r.content
    #d=re.findall('\,\"name\"\:\"(\w{1,64})\"\,\"description\"',r.content)
    d=re.findall('\{\"id\"\:(\d{4,6})\,\"name\"',r.content)
    #print d

    for ds in d:
        r=requests.get(URL+POL+'?pending=true',headers={'sid':req.json()['sid']},verify=False)
        mtag={'MTag': str(r.headers['mtag'])}
        #print mtag
        #print r.url
        pol['secpolicy']['description']=''.join(random.choice(string.printable) for i in xrange(random.randint(1,64),random.randint(128,256)))
        pol['secpolicy']['name']=''.join(random.choice(string.printable) for i in xrange(random.randint(1,32),random.randint(32,64)))
        #print pol
        #https://10.24.254.71/rest/policies/sec/1465?pending=true&_=1465996198787
        r=requests.get(URL+POL+'/{0}?pending=true'.format(ds),headers={'sid':req.json()['sid'],'MTag': str(r.headers['mtag'])},verify=False)
        #print r.url

        r=requests.put(URL+POL+'/{0}'.format(ds),json=pol,headers={'sid':req.json()['sid'],'MTag': str(r.headers['mtag'])},verify=False)
        #print r.status_code
        #print r.url
        #print r.headers

        if r.status_code == 200:
            number+=1
            print 'updated succ'
        else:
            print 'updated fail'

    p=requests.post(URL+POL+'/pending',headers={'sid':req.json()['sid']},verify=False)
    print 'updated {0} policies'.format(number)


def retrieve():
    global d11

    s1=requests.get(URL+IP+'?',headers={'sid':req.json()['sid']},verify=False)
    d1=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s1.content)
    s2=requests.get(URL+IPS+'?',headers={'sid':req.json()['sid']},verify=False)
    d2=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s2.content)
    s3=requests.get(URL+UF+'?',headers={'sid':req.json()['sid']},verify=False)
    d3=re.findall('\[\{\"id\"\:(\d{1,4})\,\"',s3.content)
    s4=requests.get(URL+AC+'?',headers={'sid':req.json()['sid']},verify=False)
    d4=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s4.content)
    s5=requests.get(URL+IPs+'?',headers={'sid':req.json()['sid']},verify=False)
    d5=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s5.content)
    s6=requests.get(URL+VLAN+'?',headers={'sid':req.json()['sid']},verify=False)
    d6=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s6.content)
    s7=requests.get(URL+VLANS+'?',headers={'sid':req.json()['sid']},verify=False)
    d7=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s7.content)
    s8=requests.get(URL+SERV+'?',headers={'sid':req.json()['sid']},verify=False)
    d8=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s8.content)
    s9=requests.get(URL+SERVS+'?',headers={'sid':req.json()['sid']},verify=False)
    d9=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s9.content)
    s10=requests.get(URL+SCHE+'?',headers={'sid':req.json()['sid']},verify=False)
    d10=re.findall('\"id\"\:(\d{1,4})\,\"name\"',s10.content)
    s11=requests.get(URL+POL+'?',headers={'sid':req.json()['sid']},verify=False)
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

    s=requests.get(URL+'/rest/vnfs',headers={'sid':req.json()['sid']},verify=False)
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

    s=requests.post(URL+'/rest/nodes',json=nodet,headers={'sid':req.json()['sid']},verify=False)
    #s=requests.delete(URL+'/rest/nodes?nodes=1',headers={'sid':req.json()['sid']},verify=False)
    print s.status_code
    print s.content
    #print nodet['node']


def del_node(node=1):
    #s=requests.delete(URL+'/rest/nodes?nodes=1',headers={'sid':req.json()['sid']},verify=False)
    s=requests.delete(URL+'/rest/nodes/'+str(node),headers={'sid':req.json()['sid']},verify=False)
    print s.status_code
    print s.content
    #print nodet['node']


acct=json.loads('{"admin":{"login":"11111111","name":"11111111","password":"11111111","email":"","email_alert":false,"description":"","admingroup":{"id":2},"passwordConfirm":"11111111"}}')

def add_account(counter=1):
    for i in range(1,counter+1):
        acct["admin"]["login"]="test"+str(i)
        acct["admin"]["name"]="test"+str(i)
        s=requests.post(URL+'/rest/admins',json=acct,headers={'sid':req.json()['sid']},verify=False)
        print s.status_code
        print s.content
        print acct
        #print nodet['node']

payload=json.loads('{"schd":{"name":"1","description":"","period":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335]}}')

def add_schds(counter=1):
    for i in range(1,counter+1):
        payload["schd"]["name"]="test"+str(i)
        s=requests.post(URL+'/rest/object/schds',json=payload,headers={'sid':req.json()['sid']},verify=False)
        print s.status_code
        print s.content
        #print payload


def add_adp(counter=3):
    if glob.glob('/tmp/adp.json'):
        sig=json.loads(open('/tmp/adp.json').read())
    else:
        a=requests.get(URL+ADP+'/1',headers={'sid':req.json()['sid']},verify=False)
        with file('/tmp/adp.json','w') as f:
            f.write(a.content)
        sig=json.loads(a.text)
    number=0

    for i in range(1,counter+1):
        sig['adProfile']['name']='test-'+str(i)
        sig['adProfile']['enabled']=True
        s=requests.post(URL+ADP,json=sig,headers={'sid':req.json()['sid']},verify=False)
        print s.status_code

        if s.status_code == 200:
            number+=1
            print 'create adp succ {0}'.format(number)
        else:
            print 'adp fail'
    print 'created {} profiles'.format(number)

def copy_adp(counter=3):
    number=0

    for i in range(1,counter+1):
        s=requests.post(URL+IPS+'/1/duplicate',headers={'sid':req.json()['sid']},verify=False)
        print s.status_code

        if s.status_code == 200:
            number+=1
            print 'create ips succ {0}'.format(number)
        else:
            print 'ips fail'
    print 'created {} profiles'.format(number)



#=====================================================================

add_adp(10)
#copy_adp(1)
#add_account(1)
#add_ips(100)
#copy_ips(1)
#del_ips()
#add_pol(1020)
#update_pol()
#del_pol()

#retrieve()
#a=retrieve()
#print d11
#fuzz()
#add_node()
#del_node(3)
#get_nodes()
#add_schds(100)
