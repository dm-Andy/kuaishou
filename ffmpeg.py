import os
import json

with open('./video.json','r',encoding='utf-8') as f:
    data = json.loads(f.read())

if not os.path.exists('./mp3'):
    os.mkdir('./mp3')

if not os.path.exists('./pcm'):
    os.mkdir('./pcm')

if not os.path.exists('./wav'):
    os.mkdir('./wav')

# for x in data:
#     filename = os.path.split(x)[1]
#     newfilename = filename.replace('.mp4','.mp3')
#     os.system('ffmpeg -i ./mp4/%s -f mp3 -vn ./mp3/%s' %(filename,newfilename))
# # 转换mp3完毕


# filenames = os.listdir('./mp3')
# for filename in filenames:
#     newfilename = filename.replace('.mp3','.pcm')
#     os.system('ffmpeg -i ./mp3/%s -f s16be -ar 16000 -ac 1 -acodec pcm_s16be ./pcm/%s' %(filename,newfilename))

filenames = os.listdir('./mp3')
for filename in filenames:
    newfilename = filename.replace('.mp3','.wav')
    os.system('ffmpeg -i ./mp3/%s -acodec pcm_s16le -y ./wav/%s' %(filename,newfilename))