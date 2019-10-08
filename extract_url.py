import json
import requests

json_path = './data.json'

UA = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}

url = 'https://live.kuaishou.com/graphql'

with open(json_path,'r',encoding='utf-8') as f:
    data = json.loads(f.read())

# 快手改了，所以先拿photoId，然后请求真实地址
lists = data['data']['publicFeeds']['list']
author = data['data']['publicFeeds']['list'][0]['user']['id']

photoIds = []
for x in lists:
    photoIds.append(x['photoId'])

query = '''query SharePageQuery($principalId: String, $photoId: String) {
  feedById(principalId: $principalId, photoId: $photoId) {
    currentWork {
      playUrl
      __typename
    }
    __typename
  }
}
'''

# 如果不能用，浏览器里面找到cookie，自己替换即可
cookies = {
  'did':'web_499b1d56248e45f79ee28125cd0508b8',
  'client_key':'65890b29'
}

playUrls = []
for x in photoIds:
    print(x)
    payload = {"operationName":"SharePageQuery",
                "variables":{"photoId":x,"principalId":author},
                "query":query}

    res = requests.post(url=url,json=payload,headers=UA,cookies=cookies)
    data = json.loads(res.text)
    playUrl = data['data']['feedById']['currentWork']['playUrl']
    playUrls.append(playUrl)

with open('video.json','w',encoding='utf-8') as f:
    f.write(json.dumps(playUrls, indent=4, separators=(',', ':')))
