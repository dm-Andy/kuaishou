import os


UA = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",\
    'content-type': 'application/json'
}

POST_URL = 'https://live.kuaishou.com/graphql'

# 如果不能用，浏览器里面找到cookie，自己替换即可
COOKIES = {
  'did':'web_499b1d56248e45f79ee28125cd0508b8',
  'client_key':'65890b29'
}

JSON_PATH = './json/'
DATA_JSON_PATH = os.path.join(JSON_PATH,'data.json')
VIDEO_JSON_PATH = os.path.join(JSON_PATH,'video.json')
IMAGE_JSON_PATH = os.path.join(JSON_PATH,'image.json')

