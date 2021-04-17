from pytube import YouTube
import pafy
from FrameExtractor import FrameExtractor

def ConvertVideoToManga(UrlList):
    for videoUrl in UrlList:
        video = YouTube(videoUrl)
        dataUrl = video.streams.get_by_itag(137).url
        compUrl = video.streams.get_by_itag(160).url
        fe = FrameExtractor(compUrl,dataUrl)
        fe.extract_distinct_frames(every_x_frame=300,
                            file_name=video.title, 
                            dest_path=video.author,
                            tolerance=10
        )
        print(f'Processing completed for : {video.title}')


def ConvertVideoUrlToUrlList(Url,UrlType):
    UrlList=[]
    if UrlType.lower() == 'playlist':
        videoPlaylistUrl = Url
        playlist = pafy.get_playlist(videoPlaylistUrl)
        for i in range(1,len(playlist['items'])+1):
            videoUrl = f"https://www.youtube.com/watch?v={playlist['items'][i-1]['playlist_meta']['encrypted_id']}&list={videoPlaylistUrl[38:]}&index={i}"
            UrlList.append(videoUrl)
    elif UrlType.lower() == 'video':
        UrlList.append(Url)
    else:
        assert 'Invalid Url type'
    # print(UrlList)
    return UrlList


videoPlaylistUrl = 'https://www.youtube.com/playlist?list=PLgdSLmf4viPfzkC5LsChx-5p1tjQh_IZd'

videoUrllist = ConvertVideoUrlToUrlList(Url=videoPlaylistUrl,
                    UrlType='playlist'
                    )

# ConvertVideoToManga(videoUrllist)




