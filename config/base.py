#coding:utf8
import paramiko,os

Base_dir = os.path.dirname(os.path.dirname(__file__))

class Paramiko:
    def __init__(self):
        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp=None

    #连接虚拟机
    def connect(self,host,port,user,pwd=None,key=None):

        try:
            self.host=host
            if pwd ==None: #私钥链接
                if key==None:
                    key=paramiko.RSAKey.from_private_key_file('id_rsa')
                    self.ssh.connect(host,port,user,pkey=key)
                else:
                    self.ssh.connect(host, port, user, pkey=key)
            else: #密码链接
                self.ssh.connect(host, port, user, pwd)
        except Exception,e:
            print str(e)

    #执行命令
    def cmd(self,cmd):
        try:
            print '-'*10+self.host+':'+cmd+'-'*10
            stdin,stdout,stderr=self.ssh.exec_command(cmd)
            for line in stdout:
                print line,

        except Exception,e:
            print str(e)

    #获取sftp对象
    def __get_sftp(self):
        # if self.sftp is not None:  #对象已经建立
        #     return self.sftp
       # else:
        #     self.sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        #     return self.sftp
        if self.sftp is None:
            self.sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        return self.sftp


    #远程上传文件
    def upload(self,local,remote):
        try:
            sftp=self.__get_sftp()
            res=sftp.put(local,remote)

        except Exception,e:
            print str(e)

    #远程下载文件
    def download(self,remote,local):
        try:
            sftp = self.__get_sftp()
            res=sftp.get(remote,local)
        except Exception,e:
            print str(e)