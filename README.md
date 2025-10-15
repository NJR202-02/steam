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

黃語婷、林雅嵐、王定國、施漢羿

# 🏗️ 專案架構概述


本專案是一個完整的資料工程管道，整合了多個現代化的資料處理工具：

- **🕷️ 資料擷取**: 使用 Python 爬蟲技術擷取 Steam遊戲平台資料
- **⚡ 任務調度**: 透過 Celery + RabbitMQ 實現分散式任務處理
- **🚀 工作流程管理**: 使用 Apache Airflow 進行 ETL 流程編排
- **🗄️ 資料存儲**: MySQL 資料庫儲存結構化資料
- **📊 資料視覺化**: Metabase 建立商業智慧儀表板
- **🐳 容器化部署**: Docker & Docker Compose 統一管理服務

### 資料流程
```
Steam API → Python 爬蟲 → RabbitMQ → Celery Workers → MySQL → Metabase
                ↑                                                ↓
            Airflow DAG                                      商業智慧報表

steam/
├── .venv/                                   # Python 虛擬環境
├── .env.example
├── .gitignore                               # Git 忽略檔案設定
├── .python-version                          # Python 版本指定
├── README.md                                # 專案說明文件
├── pyproject.toml                           # Python 專案配置檔
├── uv.lock                                  # UV 套件管理鎖定檔
├── Dockerfile                               # Docker 映像檔配置
├── main.py
│
├── airflow/                                 # 🔥 核心資料擷取模組
│   ├── dags
│       └── dag_producer_steam_scraper.py
│   ├── airflow.cfg
│   ├── docker-compose-airflow-vm.yml
│   ├── docker-compose-airflow.yml
│   └── Dockerfile
│
├── data_ingestion/                          # 🔥 核心資料擷取模組
│   ├── __init__.py                              
│   ├── scraper.py
│   ├── database
│       ├── __init__.py
│       ├── configuration.py
│       ├── schema.py
│       └── upload.py
│   ├── message_queue
│       ├── __init__.py
│       ├── configuration.py
│       ├── worker.py
│       ├── tasks.py
│       └── producer.py
│                        
├── docker_compose/
│   ├── docker-compose-broker.yml
│   ├── docker-compose-mysql-vm.yml
│   ├── docker-compose-mysql.yml
│   ├── docker-compose-producer.yml
│   ├── docker-compose-worker-vmQ.yml
│   └── docker-compose-worker.yml
│
├── infra/tf/steam-workers/
│   ├── terraform
│       ├──LICENSE.txt
│       └──terraform-provider-google_v5.45.2_x5
│   ├──terraform.lock.hcl
│   ├── main.tf
│   ├── prod.tfvars
│   ├── prod.tfvars.example
│   ├── startup.sh.tmpl
│   ├── terraform.tfstate
│   └── terraform.tfstate.backup
├── metabase/
    ├── docker-compose-metabase-vm.yml
    └── docker-compose-metabase.yml



```
git clone
```

```
uv sync
```

## 建立 docker network
```
docker network create njr20202_network
```

## MySQL
```
docker compose -f docker_compose/docker-compose-mysql.yml up -d
```

## Airflow
```
docker build -f airflow/Dockerfile -t shydatas/airflow:latest .
```

```
docker compose -f airflow/docker-compose-airflow.yml up
```

## Message Queue
```
docker build -f Dockerfile -t shydatas/data_ingestion:latest .
```

```
docker compose -f docker_compose/docker-compose-broker.yml up -d
docker compose -f docker_compose/docker-compose-producer.yml up
docker compose -f docker_compose/docker-compose-worker.yml up
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