# falcon-plus-agent-deploy
使用前自行部署fabric,修改conf/cfg.json中openfalcon-server的IP,修改manage_openFalconAgent.py中目标主机IP及认证秘钥路径
## 部署open-falcon-agent
fab -f manage_openFalconAgent.py task
## 部署redis监控插件
部署前或后需在dashboard主机组中绑定redis插件监控插件
fab -f manage_openFalconAgent.py redis_plugin

