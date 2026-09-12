"""Create a local API profile without echoing or accepting a key on the command line."""
import getpass
import json
import os
from pathlib import Path
import urllib.parse

root=Path(__file__).resolve().parents[2]
url=input('OpenAI-compatible API base URL (ending in /v1): ').strip().rstrip('/')
parsed=urllib.parse.urlsplit(url)
if parsed.scheme!='https' or not parsed.netloc or not url.endswith('/v1'):
    raise SystemExit('Use an HTTPS API base URL ending in /v1.')
key=getpass.getpass('API key (hidden): ').strip()
if not key: raise SystemExit('Empty credential')
folder=root/'.secrets';folder.mkdir(mode=0o700,exist_ok=True);folder.chmod(0o700)
path=folder/'boyu-20260912.json'
if path.exists(): raise SystemExit('Profile exists; reuse it or move it aside explicitly.')
fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w') as f:json.dump({'base_url':url,'api_key':key},f)
print('Saved private profile; never commit .secrets/.')
