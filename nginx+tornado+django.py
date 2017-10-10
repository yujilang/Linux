#coding:utf8
from paramilko_deploy.nginx_auto_deploy import *
from django_deploy.polls_deploy import *
from config import host_config

from paramilko_deploy import nginx_auto_deploy
from django_deploy import polls_deploy



if __name__ == '__main__':
    s_time = time.time()
    # 多线程

    # nginx_clients = nginx_auto_deploy.get_ssh_client(host_config.webserver)
    # nginx_list = nginx_auto_deploy.get_threads(nginx_clients)
    # nainx_start(nginx_list)
    #
    # djano_clients = polls_deploy.get_ssh_client(host_config.webserver)
    # django_list = polls_deploy.get_threads(djano_clients)
    # diango_start(django_list)
    # 单线程
    nginx_deploy(host_config.webserver)
    django_deploy()
    print '-------%d-------' % int(time.time() - s_time)