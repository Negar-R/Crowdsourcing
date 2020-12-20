from pathlib import Path
from dotenv import load_dotenv, find_dotenv


# load .env file
env_file = Path(find_dotenv(usecwd=True))
load_dotenv(verbose=True, dotenv_path=env_file)

from .redis_exe import Redis