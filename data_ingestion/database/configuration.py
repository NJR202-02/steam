import os


# MySQL
MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
# MYSQL_HOST = os.environ.get("MYSQL_HOST", "mysql")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "njr20202")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "steam")