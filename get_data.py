import requests
import json

UA = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}

url = 'https://live.kuaishou.com/graphql'

query = """query ProfileFeeds($principalId: String, $privacy: String, $pcursor: String, $count: Int) {
  getProfileFeeds(principalId: $principalId, privacy: $privacy, pcursor: $pcursor, count: $count) {
    pcursor
    live {
      ...LiveStreamInfo
      __typename
    }
    list {
      ...WorkInfo
      __typename
    }
    __typename
  }
}

fragment LiveStreamInfo on LiveStream {
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

fragment WorkInfo on VideoFeed {
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
  playUrl
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
    name
    profile
    __typename
  }
  expTag
  __typename
}
"""

author = input('输入主播的ID：')
if not author:
    author = '3xdqruzfay95yys'
# "pcursor":"1.544090000891E12"
payload = {"operationName":"ProfileFeeds",
            "variables":{"principalId":author,"privacy":"public","count":100},
            "query":query}

res = requests.post(url=url,json=payload,headers=UA)
data = json.loads(res.text)

with open('./data.json','w',encoding='utf-8') as f:
    f.write(json.dumps(data, indent=4, separators=(',', ':')))