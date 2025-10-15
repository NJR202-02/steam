# Steam 遊戲評論分析專題

Steam作為全球最大的遊戲平台，其海量用戶評論是反映玩家真實情感與需求的即時數據源。
希望透過網路爬蟲與雲端分析技術，讓遊戲開發商重視廣大玩家意見並開發人人都愛玩遊戲。

## 專案目標

建立自動化評論蒐集系統,透過資料工程技術萃取有價值訊息,運用時間序列分析找出影響玩家滿意度的關鍵因素，為遊戲開發者與發行商提供具體市場洞察,協助掌握產業趨勢,優化遊戲設計決策,最終提升玩家體驗品質。


## 組員

黃語婷、林雅嵐、王定國、施漢羿

## 🏗️ 專案架構概述

本專案是一個完整的資料工程管道，整合了多個現代化的資料處理工具：

- **🕷️ 資料擷取**: 使用 Python 爬蟲技術擷取 Steam 遊戲平台資料
- **⚡ 任務調度**: 透過 Celery + RabbitMQ 實現分散式任務處理
- **🚀 工作流程管理**: 使用 Apache Airflow 進行 ETL 流程編排
- **🗄️ 資料存儲**: MySQL 資料庫儲存結構化資料
- **📊 資料視覺化**: Metabase 建立商業智慧儀表板
- **🐳 容器化部署**: Docker & Docker Compose 統一管理服務


## 資料流程
```
Steam API → Python 爬蟲 → RabbitMQ → Celery Workers → MySQL → Metabase
                ↑                                                ↓
            Airflow DAG                                      商業智慧報表
```


## 資料夾結構
```
steam/
├── .venv/                                   # Python 虛擬環境
├── .env.example
├── .gitignore                               # Git 忽略檔案設定
├── .python-version                          # Python 版本指定
├── README.md                                # 專案說明文件
├── pyproject.toml                           # Python 專案配置檔
├── uv.lock                                  # UV 套件管理鎖定檔
├── Dockerfile                               # Docker 映像檔配置
│
├── airflow/                                 # Apache Airflow 工作流程管理
│   ├── airflow.cfg                          # Airflow 配置檔
│   ├── docker-compose-airflow-vm.yml        # Airflow-vm Docker Compose 配置
│   ├── docker-compose-airflow.yml           # Airflow Docker Compose 配置
│   ├── Dockerfile                           # Airflow Docker 映像檔
│   └── dags                                 # Airflow DAG 工作流程定義
│       └── dag_producer_steam_scraper.py    # Steam 爬蟲 DAG
│
├── data_ingestion/                          # 核心資料擷取模組
│   ├── __init__.py                          # Python 套件初始化                             
│   ├── scraper.py                           # 爬蟲基礎模組
│   ├── database
│   │   ├── __init__.py                      # Python 套件初始化
│   │   ├── configuration.py                 # 配置檔（環境變數）
│   │   ├── schema.py                        # 資料表結構
│   │   └── upload.py                        # 上傳/讀取資料庫函數
│   └── message_queue
│       ├── __init__.py                      # Python 套件初始化
│       ├── configuration.py                 # 配置檔（環境變數）
│       ├── worker.py                        # Celery Worker 設定
│       ├── tasks.py                         # Celery 任務定義
│       └── producer.py                      # 基本 Producer
│                        
├── docker_compose/
│   ├── docker-compose-broker.yml            # RabbitMQ Broker 配置
│   ├── docker-compose-mysql-vm.yml          # MySQL-vm 資料庫配置
│   ├── docker-compose-mysql.yml             # MySQL 資料庫配置
│   ├── docker-compose-producer.yml          # Producer 服務配置
│   ├── docker-compose-worker-vmQ.yml        # Worker-vm 服務配置
│   └── docker-compose-worker.yml            # Worker 服務配置
│
├── infra/tf/steam-workers/
│   ├── terraform
│   │   ├──LICENSE.txt
│   │   └──terraform-provider-google_v5.45.2_x5
│   ├──terraform.lock.hcl
│   ├── main.tf
│   ├── prod.tfvars
│   ├── prod.tfvars.example
│   ├── startup.sh.tmpl
│   ├── terraform.tfstate
│   └── terraform.tfstate.backup
│
└── metabase/
    ├── docker-compose-metabase-vm.yml       # metabase-vm 服務配置
    └── docker-compose-metabase.yml          # metabase 服務配置
```


## 指令

### 🔧 環境設定
```bash
# 建立虛擬環境並安裝依賴（同步）
uv sync
```

### 建立 docker network
```
docker network create njr20202_network
```

### MySQL 資料庫
```bash
# 啟動 MySQL 服務
docker compose -f docker_compose/docker-compose-mysql-vm.yml up -d

# 停止 MySQL 服務
docker compose -f docker_compose/docker-compose-mysql-vm.yml down
```

### Apache Airflow 工作流程管理 (待改)
```
docker build -f Dockerfile -t DOCKER_HUB_USER/data_ingestion:latest .
```

```
# 啟動 Airflow 服務
docker compose -f airflow/docker-compose-airflow.yml up
```

### Message Queue (RabbitMQ Broker 與 Celery Worker)
```
# 啟動 RabbitMQ Broker 服務
docker compose -f docker_compose/docker-compose-broker.yml up -d

# 停止並移除 RabbitMQ 服務
docker compose -f docker_compose/docker-compose-broker.yml down

docker compose -f docker_compose/docker-compose-producer.yml up
docker compose -f docker_compose/docker-compose-worker.yml up

# 查看服務 logs
docker logs -f rabbitmq
docker logs -f flower
```

### Metabase 商業智慧儀表板
```bash
# 啟動 Metabase 服務（包含 PostgreSQL）
docker compose -f metabase/docker-compose-metabase-vm.yml up -d

# 停止 Metabase 服務
docker compose -f metabase/docker-compose-metabase-vm.yml down

# 查看 Metabase 服務狀態
docker compose -f metabase/docker-compose-metabase-vm.yml ps

# 存取 Metabase 網頁介面
# http://35.209.179.160:3000/
```

###  Docker Compose 服務管理
```bash
# 啟動所有相關服務
docker compose -f docker_compose/docker-compose-broker.yml up -d
docker compose -f docker_compose/docker-compose-mysql-vm.yml up -d
docker compose -f docker_compose/docker-compose-mysql.yml up -d
docker compose -f docker_compose/docker-producer.yml up -d
docker compose -f docker_compose/docker-worker-vmQ.yml up -d
docker compose -f docker_compose/docker-worker.yml up -d

# 停止所有服務
docker compose -f docker_compose/docker-compose-broker.yml down
docker compose -f docker_compose/docker-compose-mysql-vm.yml down
docker compose -f docker_compose/docker-compose-mysql.yml down
docker compose -f docker_compose/docker-producer.yml down
docker compose -f docker_compose/docker-worker-vmQ.yml down
docker compose -f docker_compose/docker-worker.yml down
```

## Terraform 

### 1）安裝 Terraform（Ubuntu）
- 在本地Ubuntu進行安裝。
```
sudo apt update
sudo apt install -y wget gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform
```

### 2）登入 GCP（讓 Terraform 有權限）
- 授予 Terraform 建立 VM 的權限。輸入專案ID時請拿掉"<>"。
```
gcloud auth application-default login
gcloud config set project <你的GCP專案ID>
```

### 3）進入指定資料夾並建立prod.tfvars
- 可參考prod.tfvars.example建立。
- worker_count可直接決定需要的vm-worker台數。
- 先進入steam/infra/tf/steam-workers再建立prod.tfvars。

```
cd steam/infra/tf/steam-workers
```

```
nano prod.tfvars
```

### 4）初始化
```
terraform init
```

### 5）建立vm-worker
```
terraform apply -var-file=prod.tfvars -var="project_id=your project id"
```

### 6）刪除已建立vm-worker
```
terraform destroy -var-file=prod.tfvars -var="project_id=your project id"
```










