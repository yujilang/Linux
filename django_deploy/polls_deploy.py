#coding:utf8
from config.base import Paramiko
from config import host_config
import config
import os,paramiko
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
        t=threading.Thread(target=django_cmd,args=(client,))
        t_list.append(t)
    return t_list

#命令
def django_cmd(client):
    # 创建虚拟环境
    client.cmd('virtualenv /root/Desktop/python-envl/django1.8')

    # 上传项目
    client.upload(os.path.join(config.base.Base_dir, 'django_deploy', 'polls.zip'), '/project/polls.zip')
    client.cmd('unzip -d  /project -o /project/polls.zip')

    # 安装mysql-python依赖包
    client.cmd('yum -y install mysql-devel')

    # 安装项目依赖
    client.cmd('/root/Desktop/python-envl/django1.8/bin/pip install -r /project/polls/requirements')

    # supervisor安装启动
    supervisor_install(client)

    nginx_server(client)

#启动多线程
def diango_start(t_list):
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()

#-------------------------------------------------------
# supervisor安装启动
def supervisor_install(p):
    #安装红帽源
    p.cmd(r'rpm -Uvh https://mirrors.tuna.tsinghua.edu.cn/epel//7/x86_64/e/epel-release-7-10.noarch.rpm')
    p.cmd('yum -y install supervisor')
    p.upload(os.path.join(config.base.Base_dir,'django_deploy','polls.ini'),'/etc/supervisord.d/polls.ini')
    p.cmd('systemctl start supervisord.service')
    p.cmd('supervisorctl reload') #如果启动，重新加载配置文件

def nginx_server(p):
    p.upload(os.path.join(config.base.Base_dir,'django_deploy','polls_conf'),'/usr/local/nginx1.10.2/conf/vhosts.d/polls.conf')
    p.cmd('pkill nginx')
    p.cmd('nginx')

#-------------------------------------------------------


#单线程
def django_deploy():
    for host in host_config.webserver:
        p=Paramiko()
        key = paramiko.RSAKey.from_private_key_file(os.path.join(config.base.Base_dir, 'config', 'id_rsa'))
        p.connect(host=host[0],port=host[1],user=host[2],pwd=host[3])

        #创建虚拟环境
        p.cmd('virtualenv /root/Desktop/python-envl/django1.8')

        #上传项目
        p.upload(os.path.join(config.base.Base_dir,'django_deploy','polls.zip'),'/project/polls.zip')
        p.cmd('unzip -d  /project -o /project/polls.zip')

        #安装mysql-python依赖包
        p.cmd('yum -y install mysql-devel')

        #安装项目依赖
        p.cmd('/root/Desktop/python-envl/django1.8/bin/pip install -r /project/polls/requirements')

        #supervisor安装启动
        supervisor_install(p)

        nginx_server(p)



if __name__ == '__main__':
    s_time = time.time()
    # 单线程
    #django_deploy()

    # 多线程
    clients = get_ssh_client(host_config.webserver)
    t_list = get_threads(clients)
    diango_start(t_list)

    print '-------%d-------'%int(time.time()-s_time)