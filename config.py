# coding: UTF-8
# .env ファイルをロードして環境変数へ反映
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'config.env')
load_dotenv(dotenv_path)

# 環境変数を参照
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')