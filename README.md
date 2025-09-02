## 啟動 airflow 
DOCKER_IMAGE_FULL=qweasdkimo123/air_flow:0.0.4 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow

## 啟動爬蟲工人
DOCKER_IMAGE_FULL=qweasdkimo123/air_flow:0.0.4 docker stack deploy --with-registry-auth -c docker-compose-one-worker.yml airflow

## GCP 遠端manager
### 更新套件
sudo apt-get update
### 下載 docker
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

## 檢查磁碟空間
df -h
## 刪除沒被使用的 images 
(如果一直更新image並重新啟動service會使磁碟空間不斷累積，所以有此情況務必要清理以免磁碟空間不夠)

docker image prune
## 刪除所有停止中的容器
docker container prune

## 控制scheduler 定時重啟
(以下步驟都要在 manager 的雲端機器上執行)

(由於scheduler不定時會卡住，導致任務無法傳送到Rabbitmq(或Redis)進行排程，所以必須定時重啟以維持排程)
### 安裝 cron 套件
sudo apt update

sudo apt install cron
### 安裝 nano 套件 (文字編輯器)
sudo apt install cron
### 進行定時重啟編輯
1. sudo crontab -e

   (這裡需要用sudo 以root權限去編輯，否則編輯後指令無效)
   
3. 在最下方加入指令(設定為每天早上七點、晚間11點重啟)
   

   0 23 * * * /usr/bin/docker service update --force airflow_scheduler  # 台灣 07:00

   0 15 * * * /usr/bin/docker service update --force airflow_scheduler  # 台灣 23:00
   
   (時間設定原為UTC時間，因此用UTC+8的方法做時間轉換)
   (加入"/usr/bin/docker" 方便雲端機器找到 docker 以防指令失敗)

4. 設定完按Crl + O
5. 按 Enter
6. 按 Crl + X 離開編輯
