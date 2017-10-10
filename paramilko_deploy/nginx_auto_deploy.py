#coding:utf8

# 创建nginx环境
from config.base import Paramiko
from config import host_config
import config
import paramiko,os
import threading,time

#多线程
#创建所有主机连接
def get_ssh_client(hosts):
    key = paramiko.RSAKey.from_private_key_file(os.path.join(config.base.Base_dir, 'config', 'id_rsa'))
    clients=[]#所有主机连接列表
    for host in hosts:
        client= Paramiko()
        client.connect(host=host[0], port=host[1], user=host[2], key=key)  # 建立连接
        clients.append(client)
    return clients

#创建多线程
def get_threads(clients):
    t_list=[]
    for client in clients:
        t=threading.Thread(target=nginx_cmd,args=(client,))
        t_list.append(t)
    return t_list

#命令
def nginx_cmd(client):
    client.upload(os.path.join(config.base.Base_dir, 'paramilko_deploy', 'Desktop.zip'), '/opt/nginx.zip')
    client.cmd('unzip -o -d /opt/ /opt/nginx.zip  ')
    client.cmd('python /opt/nginx.py')

#启动多线程
def nainx_start(t_list):
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()


#单线程
def nginx_deploy(hosts):
    for host in hosts:
        p= Paramiko()
        key = paramiko.RSAKey.from_private_key_file(os.path.join(config.base.Base_dir, 'config', 'id_rsa'))
        p.connect(host=host[0],port=host[1],user=host[2],pwd=host[3]) #建立连接
        p.upload(os.path.join(config.base.Base_dir,'paramilko_deploy','Desktop.zip'),'/opt/nginx.zip')
        p.cmd('unzip -o -d /opt/ /opt/nginx.zip  ')
        p.cmd('python /opt/nginx.py')

if __name__ == '__main__':
    s_time=time.time()
    #多线程
    clients=get_ssh_client(host_config.webserver)
    t_list=get_threads(clients)
    nainx_start(t_list)
    #单线程
    #nginx_deploy(host_config.webserver)
    print '-------%d-------'%int(time.time()-s_time)