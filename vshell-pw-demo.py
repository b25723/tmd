import paramiko
import socket
import time
import logging
import string
import random
import sys

host=sys.argv[1]
#host='10.24.254.181'
user='root'
initpw="ntdtg@trendmicro"
psw="""ntdtg@trendmicro"""

#0=match and min/max,1=unmatch,2=perhaps match
def gen(inp=0):
    #chs=map(chr,range(32,127))
    digits=map(chr,range(48,58))
    symbols=map(chr,range(32,48)+range(58,65)+range(91,97)+range(123,127))
    upletters=list(string.ascii_uppercase)
    lowletters=list(string.lowercase)
    ctrlchars=map(chr,range(0,32))
    extendchars=map(unichr,range(127,256))
    if inp==0:
        comb=digits+symbols+upletters+lowletters
        pos_padding=''.join([random.choice(comb) for x in range(random.randint(4,28))])
        out=random.choice(digits)+random.choice(symbols)+random.choice(upletters)+random.choice(lowletters)+pos_padding
        print len(out)
        print map(ord,out)
        print out
        return out
    elif inp==1:
        comb=digits+symbols+upletters+lowletters+ctrlchars+extendchars
        neg_padding=''.join([random.choice(comb) for x in range(random.randint(2,30))])
        out=random.choice(digits)+random.choice(symbols)+random.choice(upletters)+random.choice(lowletters)+neg_padding
        print len(out)
        print map(ord,out)
        print out
        return out
    elif inp==2:
        comb=random.choice([digits+symbols+upletters,digits+symbols+upletters+lowletters,digits+symbols+upletters+lowletters+ctrlchars+extendchars])
        neg_padding=''.join([random.choice(comb) for x in range(random.randint(4,28))])
        out=random.choice(digits)+random.choice(symbols)+random.choice(upletters)+neg_padding
        print len(out)
        print map(ord,out)
        print out
        return out

def login(password=psw):
    global psw
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,username=user,password=password,timeout=30)
    channel = ssh.invoke_shell()
    psw=gen(0)
    time.sleep(1)
    channel.send('passwd\n')
    channel.send(psw+'\n')
    time.sleep(1)
    channel.send(psw+'\n')
    time.sleep(1)
    ssh.close()

#for i in range(10):gen(2)
for i in range(10000):
    try:
        #print psw
        login(password=psw)
        #print psw
    except (socket.error, NameError) as e:
        print e
        pass

