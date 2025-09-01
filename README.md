## 啟動 airflow 
DOCKER_IMAGE_FULL=qweasdkimo123/air_flow:0.0.4 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow

## 啟動爬蟲工人
DOCKER_IMAGE_FULL=qweasdkimo123/air_flow:0.0.4 docker stack deploy --with-registry-auth -c docker-compose-one-worker.yml airflow

## GCP 遠端manager
### 更新套件
sudo apt-get update
### 下載
sudo apt-get install docker.io
### 加入docker群組
sudo usermod -aG docker $USER
### 登入docker帳號
docker login -u <docker帳號>
### 重新登入
newgrp docker
### 測試docker指令
docker ps
### 離開docker swarm
docker swarm leave --force
### swarm 初始化(初始化後的token 須記下)
docker swarm init
### 加入node
(在其他雲端機器裡輸入以下指令使其加入node裡成為manager的worker)
docker swarm join --token <你的token>
### 建立docker內網 
(如果不對外開port 就必須要內網連結各台機器，且機器所在的區域必須是同一個)
docker network create --scope=swarm --driver=overlay --attachable my_swarm_network
### 建立volume
docker volume create mysql
### 刪除volume
docker volume rm mysql

### 檢查磁碟空間
df -h
### 刪除沒被使用的 images 
(如果一直更新image並重新啟動service會使磁碟空間不斷累積，所以有此情況務必要清理以免磁碟空間不夠)
docker image prune
### 刪除所有停止中的容器
docker container prune
