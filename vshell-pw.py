import paramiko
import socket
import time
import logging
import string
import random

#host='10.24.253.248'
host='10.24.254.181'
user='root'
initpw="aA@1234567"
psw="""aA@1234567"""

#0=match and min/max,1=unmatch
def gen(inp=0):
    #chs=map(chr,range(32,127))
    digits=map(chr,range(48,58))
    symbols=map(chr,range(32,48)+range(58,65)+range(91,97)+range(123,127))
    upletters=list(string.ascii_uppercase)
    lowletters=list(string.lowercase)
    ctrlchars=map(chr,range(0,32))
    extendchars=map(chr,range(127,256))
    if inp==0:
        comb=digits+symbols+upletters+lowletters
        pos_padding=''.join([random.choice(comb) for x in range(random.randint(4,28))])
        out=random.choice(digits)+random.choice(symbols)+random.choice(upletters)+random.choice(lowletters)+pos_padding
        print len(out)
        print out
        return out
    elif inp==1:
        comb=digits+symbols+upletters+lowletters+ctrlchars+extendchars
        neg_padding=''.join([random.choice(comb) for x in range(random.randint(2,30))])
        out=random.choice(digits)+random.choice(symbols)+random.choice(upletters)+random.choice(lowletters)+neg_padding
        print len(out)
        print out
        return out
    elif inp==2:
        comb=random.choice([digits+symbols+upletters,digits+symbols+upletters+lowletters,digits+symbols+upletters+lowletters+ctrlchars+extendchars])
        neg_padding=''.join([random.choice(comb) for x in range(random.randint(4,28))])
        out=random.choice(digits)+random.choice(symbols)+random.choice(upletters)+neg_padding
        print len(out)
        print out
        return out

def login(password=psw):
    global psw
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,username=user,password=password,timeout=30)
    channel = ssh.invoke_shell()
    channel.send('passwd\n')
    #time.sleep(1)
    psw=gen(1)
    channel.send(psw+'\n')
    time.sleep(1)
    channel.send(psw+'\n')
    ssh.close()

#for i in range(10):gen(2)
for i in range(10000):
    try:
        #print psw
        login(password=initpw)
        #print psw
    except (socket.error, NameError) as e:
        print e
        pass




