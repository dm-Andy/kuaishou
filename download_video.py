import requests
import json
import os


UA = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}

with open('./video.json','r',encoding='utf-8') as f:
    data = json.loads(f.read())

if not os.path.exists('./mp4'):
    os.mkdir('./mp4')

for x in data:
    filename = os.path.split(x)[1]
    res = requests.get(x,headers=UA)
    with open('./mp4/'+filename,'wb') as f:
        f.write(res.content)
