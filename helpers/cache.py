import requests_cache

requests_cache.install_cache('lol_api_cache', expire_after=3600)