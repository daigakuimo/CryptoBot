# coding: UTF-8
# .env ファイルをロードして環境変数へ反映
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'config.env')
load_dotenv(dotenv_path)

# 環境変数を参照
COINCHECK_ACCESS_KEY = os.getenv('COINCHECK_ACCESS_KEY')
COINCHECK_SECRET_KEY = os.getenv('COINCHECK_SECRET_KEY')
# 環境変数を参照
GMO_ACCESS_KEY = os.getenv('GMO_ACCESS_KEY')
GMO_SECRET_KEY = os.getenv('GMO_SECRET_KEY')