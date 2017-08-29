import paramiko
import time

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.24.254.50',username='root',password='aA1 12345')
stdin,stdout,stderr=ssh.exec_command('get_ems')
print stdout.read()
