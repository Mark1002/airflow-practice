# BigAirflow

本地端開發:

1.clone project
```
git clone http://biglab.buygta.today/CrawlersV2/bigairflow.git
cd bigairflow
```

2.在環境變數設定FERNET_KEY

生一組FERNET_KEY
```
docker run puckel/docker-airflow python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)"
```

貼到.envrc
```
export FERNET_KEY=...
```

3.啟bigairflow docker-compose
```
docker-compose -f docker-compose-LocalExecutor.yml up -d --build
```

4.到127.0.0.1:8080/admin/connection/設定Connections ID

e.g.
```
Conn Id: ssh_docker_airflow(依據SSHOperator的ssh_conn_id)
Conn Type: SSH
Host  : xxx.xxx.x.xxx
Username: bignet
Password  : ***************
```


5.DAG on
