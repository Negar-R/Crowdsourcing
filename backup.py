import os
import datetime
import subprocess

from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

from pathlib import Path
from dotenv import load_dotenv, find_dotenv


# load .env file
env_file = Path(find_dotenv(usecwd=True))
load_dotenv(verbose=True, dotenv_path=env_file)

backup_dir = os.environ.get('BACKUP_DIR')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
db_host = os.environ.get('DB_HOST_LOCAL')
db_port = os.environ.get('DB_PORT_LOCAL')

if not os.path.exists(backup_dir):
    os.mkdir(backup_dir)

cmd = ["dump", "backup",
       "--dbname", f"{db_name}",
       "--username", f"{db_user}",
       "--password", f"{db_pass}",
       "--host", f"{db_host}",
       "--port", db_port,
       "--dir", f"{backup_dir}",
       "tasks_taskmodel", "accounts_userprofile", "auth_user"]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)

print(p)

minioClient = Minio("localhost:9000",
                    access_key=os.environ.get('MINIO_ACCESS_KEY'),
                    secret_key=os.environ.get('MINIO_SECRET_KEY'),
                    secure=False)

try:
    minioClient.make_bucket("backups")
except (BucketAlreadyOwnedByYou, BucketAlreadyExists) as err:
    pass
except ResponseError as err:
    raise

for file in os.listdir(backup_dir):
    file_path = os.path.join(backup_dir, file)
    minioClient.fput_object(
        "backups",
        f"{datetime.datetime.now()}_{file}",
        file_path)

os.system(f"rm -rf {backup_dir}")
