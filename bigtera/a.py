import requests
import sys
import os

addr=sys.argv[1]

print addr

def run(addr):
    resp=requests.get('https://'+addr+':8080/cgi-bin/ezs3/login?user_id=admin&password=admin',verify=False)
    conn=requests.get('https://'+addr+':8080/cgi-bin/ezs3/user_list',cookies=resp.cookies,verify=False)
    print conn.content
    print requests.get('https://'+addr+':8080/cgi-bin/ezs3/create_shared_folder?name=b0911659930&nfs=true&smb=true&read_only=false&mode=sync&user_list=b0911659930',cookies=resp.cookies,verify=False).content
#    requests.get('https://'+addr+':8080/cgi-bin/ezs3/edit_shared_folder?name=python&nfs=false&smb=true&read_only=false&mode=sync',cookies=resp.cookies,verify=False).content
#    requests.get('https://'+addr+':8080/cgi-bin/ezs3/disable_shared_folder?name=nas1',cookies=resp.cookies,verify=False).content
#    requests.get('https://'+addr+':8080/cgi-bin/ezs3/enable_shared_folder?name=nas1',cookies=resp.cookies,verify=False).content
#    requests.get('https://'+addr+':8080/cgi-bin/ezs3/delete_shared_folder?name=nas1',cookies=resp.cookies,verify=False).content
    print requests.get('https://'+addr+':8080/cgi-bin/ezs3/add_user?user_id=b0911659930&display_name=b0911659930&email=b0911659930@gmail.com&password=admin&confirm_password=admin',cookies=resp.cookies,verify=False).content
    print requests.get('https://'+addr+':8080/cgi-bin/ezs3/list_shared_folder',cookies=resp.cookies,verify=False).content
    print os.system('mount -t cifs //10.24.9.249/b0911659930 /mnt/image -o user=b0911659930,pass=admin')
    print os.system('cd /mnt/image && fio -direct=1 -iodepth 1 -thread -ioengine=libaio -bs=4k -size=100m -numjobs=1 -rw=read -name=remote_test_4k -output=statistics.txt')
    print os.system('cd /mnt/image && rsync ./test.1.0 /tmp/ --progress -avh')

run(addr)





#requests.get('https://'+addr+':8080/cgi-bin/ezs3/create_shared_folder?name=b0911659930&nfs=true&smb=true&read_only=false&mode=sync&user_list=b0911659930',cookies=resp.cookies,verify=False).content
#requests.get('https://'+addr+':8080/cgi-bin/ezs3/edit_shared_folder?name=python&nfs=false&smb=true&read_only=false&mode=sync',cookies=resp.cookies,verify=False).content
#requests.get('https://'+addr+':8080/cgi-bin/ezs3/disable_shared_folder?name=nas1',cookies=resp.cookies,verify=False).content
#requests.get('https://'+addr+':8080/cgi-bin/ezs3/enable_shared_folder?name=nas1',cookies=resp.cookies,verify=False).content
#requests.get('https://'+addr+':8080/cgi-bin/ezs3/delete_shared_folder?name=nas1',cookies=resp.cookies,verify=False).content
#requests.get('https://'+addr+':8080/cgi-bin/ezs3/list_shared_folder',cookies=resp.cookies,verify=False).content
#requests.get('https://'+addr+':8080/cgi-bin/ezs3/add_user?user_id=b0911659930&display_name=b0911659930&email=b0911659930@gmail.com&password=admin&confirm_password=admin',cookies=resp.cookies,verify=False).content
#
#requests.get('https://10.24.9.250:8080/cgi-bin/ezs3/json/list_all_nodes',cookies=req.cookies,verify=False).content
#requests.get('https://10.24.9.250:8080/cgi-bin/ezs3/json/realtime_statistic?categories=cpu_realtime',cookies=req.cookies,verify=False).content

