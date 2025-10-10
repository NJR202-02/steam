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
│   ├── scraper.py                           # 爬蟲
│   │
│   ├── database
│   │   ├── __init__.py
│   │   ├── configuration.py
│   │   ├── schema.py
│   │   └── upload.py
│   │
│   ├── message_queue
│   │   ├── __init__.py
│   │   ├── configuration.py
│   │   ├── worker.py
│   │   ├── tasks.py
│   │   └── producer.py
│   │
│   ├── docker_compose
│   │   ├── docker-compose-mysql.yml
│   │   ├── docker-compose-broker.yml
│   │   ├── docker-compose-producer.yml
│   │   └── docker-compose-worker.yml
│   │
├── airflow/                          # 🔥 核心資料擷取模組
│   ├── airflow.cfg
│   ├── docker-compose-airflow.yml
│   ├── Dockerfile
│   │
│   ├── dags
│   │   ├── __init__.py
│   │
└── 
```

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
```
sudo apt update
sudo apt install -y wget gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform
```
### 2）登入 GCP（讓 Terraform 有權限）
```
gcloud auth application-default login
gcloud config set project <你的GCP專案ID>
```
### 3）進入指定資料夾並建立prod.tfvars
可參考prod.tfvars.example建立。
worker_count可直接決定需要的vm-worker台數。
```
cd steam/infra/tf/steam-workers
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