#!/usr/local/bin/python2
# -*- coding:utf-8 -*-
from fabric.api import *
from fabric.colors import red, green
import threading
import subprocess
import sys

env.parallel = True
env.user = 'root'
env.key_filename = "/var/root/tx_masterkey.dms"
# 单个IP配置
env.hosts=['10.20.0.51']
# 多IP配置
env.hosts=['10.20.0.{}'.format(x) for x in range(1,255)]
# 单IP加多IP配置
#env.hosts = env.hosts + ['10.20.0.70']

def f_deploy():
    run('mkdir -pv /Application/falcon-agent')
    put('falcon-agent-5.1.2.tar.gz', '/Application/falcon-agent')
    run('tar -xf /Application/falcon-agent/falcon-agent-5.1.2.tar.gz -C /Application/falcon-agent')
 
def f_start():
    put('conf/cfg.json','/Application/falcon-agent')
    run('bash /Application/falcon-agent/control start')

def f_stop():
    run('bash /Application/falcon-agent/control stop')

def redis_plugin():
    run('mkdir -pv /Application/falcon-agent/plugin/redis')
    put('plugins/*redis*.py','/Application/falcon-agent/plugin/redis',mirror_local_mode=True)
    run('bash /Application/falcon-agent/control stop')
    run('bash /Application/falcon-agent/control start')
   
def go():
    execute(f_deploy)
    execute(f_start)

@runs_once
def ping():
    def ping_host(ipaddr):
        if subprocess.call('ping -c1 -W 1 %s > /dev/null' % ipaddr, shell=True) == 0:
            sys.stdout.write(green('%s is UP \n' % ipaddr))
        else:
            sys.stdout.write(red('%s is DOWN \n' % ipaddr))
    ThreadList = []
    for ip in env.hosts:
         t = threading.Thread(target=ping_host,args=(ip,))
         ThreadList.append(t)
    for t in ThreadList:
         t.start()
    for t in ThreadList:
         t.join()
