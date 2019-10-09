import requests
import json
from config import UA,POST_URL,COOKIES,DATA_JSON_PATH,VIDEO_JSON_PATH,IMAGE_JSON_PATH,JSON_PATH
import os
import shutil

# 获取主播所有作品数据
def get_data(author):
    print('准备获取主播作品数据...')
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
    payload = {"operationName":"publicFeedsQuery",
                "variables":{"principalId":author,"pcursor":"","count":10000},
                "query":query}

    res = requests.post(url=POST_URL,json=payload,headers=UA,cookies=COOKIES)
    res.encoding = 'utf-8'
    data = json.loads(res.text)

    with open(DATA_JSON_PATH,'w',encoding='utf-8') as f:
        f.write(json.dumps(data, indent=4, separators=(',', ':')))
    print('主播作品数据获取成功...')
    print()

# 提取视频、图片真实地址
def extract_url():
    print('开始分析文件地址...')
    user,urls,lines = prepare_extract_url()
    
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
    videos = {}
    imgs = []
    for x in lines:
        print(x['caption'])
        payload = {"operationName":"SharePageQuery",
                    "variables":{"photoId":x['photoId'],"principalId":user['id']},
                    "query":query}

        if x['workType'] == 'video':
            res = requests.post(url=POST_URL,json=payload,headers=UA,cookies=COOKIES)
            data = json.loads(res.text)
            playUrl = data['data']['feedById']['currentWork']['playUrl']
            # videos.append(playUrl)
            videos[x['caption']] = playUrl
        else:
            imgs += x['imgUrls']

    with open(VIDEO_JSON_PATH,'w',encoding='utf-8') as f:
        f.write(json.dumps(videos, indent=4, separators=(',', ':')))

    with open(IMAGE_JSON_PATH,'w',encoding='utf-8') as f:
        f.write(json.dumps(imgs, indent=4, separators=(',', ':')))
    
    print('分析完成...')
    print()
    return user

def prepare_extract_url():
    with open(DATA_JSON_PATH,'r',encoding='utf-8') as f:
        from_data = json.loads(f.read())

    lists = from_data['data']['publicFeeds']['list']
    user = lists[0]['user']

    urls = []
    lines = []
    for x in lists:
        urls.append('https://live.kuaishou.com/u/{author}/{photoId}?did={did}'\
            .format(author=user['id'],photoId=x['photoId'],did=COOKIES['did']))
        
        lines.append({'photoId':x['photoId'],\
            'workType':x['workType'],\
                'imgUrls':x['imgUrls'],\
                    'caption':x['caption']})

    file_path = './files/%s'%user['name']
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    os.makedirs(file_path)

    return (user,urls,lines)

def download_video(user):
    print('准备下载视频...')
    with open(VIDEO_JSON_PATH,'r',encoding='utf-8') as f:
        data = json.loads(f.read())
    path = './files/%s/videos'%user['name']
    if not os.path.exists(path):
        os.mkdir(path)

    for name,url in data.items():
        res = requests.get(url,headers=UA)
        with open(os.path.join(path,name),'wb') as f:
            f.write(res.content)
        print(name)
    print('视频下载完成...')
    print()

def download_image(user):
    print('准备下载图片...')
    with open(IMAGE_JSON_PATH,'r',encoding='utf-8') as f:
        data = json.loads(f.read())

    path = './files/%s/images'%user['name']
    if not os.path.exists(path):
        os.mkdir(path)

    for x in data:
        res = requests.get(x,headers=UA)
        name = os.path.split(x)[1]
        with open(os.path.join(path,name),'wb') as f:
            f.write(res.content)
        print(name)
    print('图片下载完成...')
    print()

def main():
    author = input('输入主播的ID：') # https://live.kuaishou.com/profile/3xdqruzfay95yys
    if not author:
        author = '3xdqruzfay95yys'
    
    if not os.path.exists(JSON_PATH):
        os.makedirs(JSON_PATH)

    get_data(author)
    user = extract_url()
    download_video(user)
    download_image(user)
    print('全部结束')

if __name__ == '__main__':
    main()
