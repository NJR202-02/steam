

# 前言

Steam作為全球最大的遊戲平台，其海量用戶評論是反映玩家真實情感與需求的即時數據源。
希望透過網路爬蟲與雲端分析技術，讓遊戲開發商重視廣大玩家意見並開發人人都愛玩遊戲。

# 分析主題：Steam熱度聲量

分析主要討論遊戲好感度、價格、消費者情緒傾向
探討單一遊戲飲在各大社群平台（上的聲量與熱度變化
尋找品牌聲量高峰與事件關聯（行銷、爭議等）

# 研究目的

幫助開發商精確識別痛點、優化產品，並快速洞察市場趨勢，從而制定高價值商業決策。


# 組員

04 黃語婷 

05 林雅嵐 

19 王定國  

22 施漢羿

# 🏗️ 專案架構概述


本專案是一個完整的資料工程管道，整合了多個現代化的資料處理工具：

- **🕷️ 資料擷取**: 使用 Python 爬蟲技術擷取 Hahow 線上課程平台資料
- **⚡ 任務調度**: 透過 Celery + RabbitMQ 實現分散式任務處理
- **🚀 工作流程管理**: 使用 Apache Airflow 進行 ETL 流程編排
- **🗄️ 資料存儲**: MySQL 資料庫儲存結構化資料
- **📊 資料視覺化**: Metabase 建立商業智慧儀表板
- **🐳 容器化部署**: Docker & Docker Compose 統一管理服務

### 資料流程
```
Steam API → Python 爬蟲 → RabbitMQ → Celery Workers → MySQL → Metabase
                ↑                                                    ↓
            Airflow DAG                                         商業智慧報表
```

## 資料夾結構
```
de-project/
├── .venv/                                   # Python 虛擬環境
├── .gitignore                               # Git 忽略檔案設定
├── .python-version                          # Python 版本指定
├── README.md                                # 專案說明文件
├── pyproject.toml                           # Python 專案配置檔
├── uv.lock                                  # UV 套件管理鎖定檔
│
├── data_ingestion/                          # 🔥 核心資料擷取模組
│   ├── __init__.py                          # Python 套件初始化
│   ├── scraper.py                           # Steam遊戲評論爬蟲
│   │
│   ├── database                             
│   │   ├── __init__.py                     # Python 套件初始化 
│   │   ├── configuration.py                # Database 環境配置檔
│   │   ├── schema.py                       # Metabase 連線表格模組
│   │   └── upload.py                       # MySQL 連線模組
│   │
│   ├── message_queue                           #  相關模組
│       ├── __init__.py                         # Python 套件初始化
│       ├── configuration.py                    # message_queuese 環境配置檔
│       ├── worker.py                           # Celery Worker 設定
│       ├── tasks.py                            # Celery 任務定義
│       └── producer.py                         # Steam遊戲評論Producer
│   
│── docker_compose                              # Docker Compose 檔案
│   ├── docker-compose-broker.yml               # RabbitMQ Broker 配置
│   ├── docker-compose-mysql.yml                # MySQL 資料庫配置
│   ├── docker-compose-mysql-vm.yml             # MySQL 雲端資料庫配置
│   ├── docker-compose-producer.yml             # Producer 服務配置
│   ├── docker-compose-worker-vm.yml            # Worker 雲端服務配置
│   ├── docker-compose-worker-vmQ.yml           # Worker 服務配置
│   └── docker-compose-worker.yml               # Worker 服務配置
│
│
│─── airflow/                                # 🚀 Apache Airflow 工作流程管理
│   ├── airflow.cfg                          # Airflow 配置檔
│   ├── Dockerfile                           # Airflow Docker 映像檔
│   ├── docker-compose-airflow.yml           # Airflow Docker Compose 配置
│   └── dags/                                # Airflow DAG 工作流程定義
│       ├── dag_producer_steam_scraper.py    # Steam Producer DAG 
│




```
## 指令

### 🔧 環境設定
```bash

# 建立虛擬環境並安裝依賴（同步）
uv sync

## 建立一個 network 讓各服務能溝通
docker network create njr20202_netwo
```


## 建立 docker network
```
docker network create njr20202_network
```


### 🚀 Apache Airflow 工作流程管理
```bash

# 建立Airflow 映像檔

docker build -f airflow/Dockerfile -t DOCKER_HUB_USER/airflow:latest .

# 啟動 Airflow 服務
docker compose -f airflow/docker-compose-airflow.ymil up -d

# 停止 Airflow 服務
docker compose -f airflow/docker-compose-airflow.yml down

# 查看 Airflow 服務狀態
docker compose -f airflow/docker-compose-airflow.yml ps


# 存取 Airflow 網頁介面
# http://localhost:8080
# 預設帳號密码: airflow / airflow
```


### 🗄️ MySQL 資料庫
```bash
# 啟動 MySQL 服務
docker compose -f docker-compose-mysql.yml up -d

# 停止 MySQL 服務
docker compose -f docker-compose-mysql.yml down
```

### 🔥 RabbitMQ Broker 與 Celery Worker
```bash
## Message Queue

docker build -f Dockerfile -t DOCKER_HUB_USER/data_ingestion:latest .

# 啟動 RabbitMQ Broker 服務
docker compose -f docker_compose/docker-compose-broker.yml up -d

# 停止並移除 RabbitMQ 服務
docker compose -f docker_compose/docker-compose-broker.yml down

# 存取 RabbitMQ 管理介面: http://localhost:15672 (guest/guest)
# 存取 Flower 監控介面: http://localhost:5555
```


### 🐳 Docker Compose 服務管理
```bash
# 啟動所有相關服務
docker compose -f docker-compose-broker.yml up -d
docker compose -f docker-compose-mysql.yml up -d
docker compose -f airflow/docker-compose-airflow.yml up -d
docker compose -f metabase/docker-compose-metabase-vm.yml up -d

# 停止所有服務
docker compose -f docker-compose-broker.yml down
docker compose -f docker-compose-mysql.yml down
docker compose -f airflow/docker-compose-airflow.yml down
docker compose -f metabase/docker-compose-metabase.yml down

# 查看所有容器狀態
docker ps -a
```






