from config.base import Paramiko
from config import host_config
import config,os,paramiko


def del_all(hosts):
    for host in hosts:
        p= Paramiko()
        key = paramiko.RSAKey.from_private_key_file(os.path.join(config.base.Base_dir, 'config', 'id_rsa'))
        p.connect(host=host[0],port=host[1],user=host[2],pwd=host[3])

        p.cmd('pkill nginx')
        p.cmd('supervisorctl stop polls')
        p.cmd('rm -rf /etc/supervisord.d/polls.ini')
        p.cmd('rm -rf /usr/local/nginx1.10.2')
        p.cmd('rm -rf /usr/local/sbin/nginx')
        p.cmd('rm -rf /project/baidu*')
        p.cmd('rm -rf /root/Desktop/python-envl/django1.8')
        p.cmd('yum -y remove supervisor')


if __name__ == '__main__':
    del_all(host_config.webserver)