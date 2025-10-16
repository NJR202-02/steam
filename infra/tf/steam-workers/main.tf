terraform {
  required_version = ">= 1.6"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.40"
    }
  }
}

# ===== 參數 =====
variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

# 單一區用 zone，多區就填 zones 清單（擇一）
variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "zones" {
  type    = list(string)
  default = ["us-central1-a", "us-central1-b", "us-central1-c", "us-central1-f"]
}

variable "worker_count" {
  type    = number
  default = 2
}

variable "machine_type" {
  type    = string
  default = "e2-micro"
}

# 一次開放多個連接埠
variable "opened_ports" {
  type    = list(string)
  default = ["3000", "3306", "5555", "5672", "8000", "8080", "15672", "22"]
}

# .env 內容（敏感資訊用 tfvars 覆蓋）
variable "env_text" {
  type    = string
  default = ""
}

# repo & compose 檔路徑（必要時可調）
variable "repo_url" {
  type    = string
  default = "https://github.com/NJR202-02/steam.git"
}

variable "compose_broker" {
  type    = string
  default = "docker_compose/docker-compose-broker.yml"
}

variable "compose_worker" {
  type    = string
  default = "docker_compose/docker-compose-worker-vmQ.yml"
}

provider "google" {
  project = var.project_id
  region  = var.region
  # zone 改由 resource 指定，方便多區分散
}

# ===== 只對 steam-worker 標籤的機器開這些 port =====
resource "google_compute_firewall" "allow_worker_ports" {
  name    = "allow-worker-ports"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = var.opened_ports
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["steam-worker"]
}

# ===== N 台 VM（可 round-robin 多個 zone） =====
resource "google_compute_instance" "worker" {
  count        = var.worker_count
  name         = "steam-worker-${count.index}"
  machine_type = var.machine_type

  # 綁防火牆用
  tags = ["steam-worker"]

  # 多區分散或單一區
  zone = length(var.zones) > 0 ? var.zones[count.index % length(var.zones)] : var.zone

  boot_disk {
    initialize_params {
      # Ubuntu 22.04 LTS 家族
      image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
      # 標準永久磁碟 10GB
      type = "pd-standard"
      size = 10
    }
  }

  network_interface {
    network = "default"
    # 臨時外網 IP，使用「標準級」網路服務
    access_config {
      network_tier = "STANDARD"
    }
  }

  # 開機腳本（外部模板檔）
  metadata_startup_script = templatefile("${path.module}/startup.sh.tmpl", {
    env_text       = var.env_text
    repo_url       = var.repo_url
    compose_broker = var.compose_broker
    compose_worker = var.compose_worker
  })
}

output "workers" {
  value = [for i in google_compute_instance.worker : { name = i.name, zone = i.zone }]
}