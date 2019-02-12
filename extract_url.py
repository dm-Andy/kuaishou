import json


json_path = './data.json'

with open(json_path,'r',encoding='utf-8') as f:
    data = json.loads(f.read())

lists = data['data']['getProfileFeeds']['list']
tmp_data = [x['playUrl'] for x in lists]

with open('video.json','w',encoding='utf-8') as f:
    f.write(json.dumps(tmp_data, indent=4, separators=(',', ':')))
