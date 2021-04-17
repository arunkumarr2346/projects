from pytube import YouTube
import os
# videoUrl =  'https://www.youtube.com/watch?v=fw2YqxfZ1dg&list=PLgdSLmf4viPfzkC5LsChx-5p1tjQh_IZd&index=14'
download_path='/home/arunkumarr2346/downloads/'

# video = YouTube(videoUrl)
# video.streams.filter(file_extension = "mp4").all()
# video.streams.get_by_itag(22).download(output_path=download_path)

# will download the highest quality progressive download stream available.
# YouTube(videoUrl).streams.first().download(output_path=download_path)

videoUrllist=[
 'https://www.youtube.com/watch?v=5OC1Gzyj8p8&list=PLgdSLmf4viPfzkC5LsChx-5p1tjQh_IZd&index=28',
 'https://www.youtube.com/watch?v=2-y4LdEGrYE&list=PLgdSLmf4viPfzkC5LsChx-5p1tjQh_IZd&index=29',
 'https://www.youtube.com/watch?v=ryy88Rmw6E4&list=PLgdSLmf4viPfzkC5LsChx-5p1tjQh_IZd&index=30',
 'https://www.youtube.com/watch?v=ic1Q69J3Qu4&list=PLgdSLmf4viPfzkC5LsChx-5p1tjQh_IZd&index=31',
 'https://www.youtube.com/watch?v=jpdjxxog3NI&list=PLgdSLmf4viPfzkC5LsChx-5p1tjQh_IZd&index=32',
 ]

for videoUrl in videoUrllist:
    video = YouTube(videoUrl)
    checkFile = f'{download_path}{video.title}.mp4'
    if os.path.isfile(checkFile):
        pass
    else:
        print(f'download started for : {video.title}')
        video.streams.first().download(output_path=download_path)
        # video.streams.get_by_itag(136).download(output_path=download_path)
    print(f'download completed for : {video.title}')