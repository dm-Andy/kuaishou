import requests
import json

UA = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}

url = 'https://live.kuaishou.com/graphql'

query = '''
query publicFeedsQuery($principalId: String, $pcursor: String, $count: Int) {
  publicFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {
    pcursor
    live {
      user {
        id
        kwaiId
        eid
        profile
        name
        living
        __typename
      }
      watchingCount
      src
      title
      gameId
      gameName
      categoryId
      liveStreamId
      playUrls {
        quality
        url
        __typename
      }
      followed
      type
      living
      redPack
      liveGuess
      anchorPointed
      latestViewed
      expTag
      __typename
    }
    list {
      photoId
      caption
      thumbnailUrl
      poster
      viewCount
      likeCount
      commentCount
      timestamp
      workType
      type
      useVideoPlayer
      imgUrls
      imgSizes
      magicFace
      musicName
      location
      liked
      onlyFollowerCanComment
      relativeHeight
      width
      height
      user {
        id
        eid
        name
        profile
        __typename
      }
      expTag
      __typename
    }
    __typename
  }
}
'''
# https://live.kuaishou.com/profile/3xdqruzfay95yys
author = input('输入主播的ID：')
if not author:
    author = '3xdqruzfay95yys'
payload = {"operationName":"publicFeedsQuery",
            "variables":{"principalId":author,"pcursor":"","count":10000},
            "query":query}

# 如果不能用，浏览器里面找到cookie，自己替换即可
cookies = {
  'did':'web_499b1d56248e45f79ee28125cd0508b8',
  'client_key':'65890b29'
}
res = requests.post(url=url,json=payload,headers=UA,cookies=cookies)
data = json.loads(res.text)

with open('./data.json','w',encoding='utf-8') as f:
    f.write(json.dumps(data, indent=4, separators=(',', ':')))