from django.shortcuts import render
from django.conf import settings
from isodate import parse_duration
import requests

# this YouTube search app is using YouTube Data API (https://developers.google.com/youtube/v3)


def index(response):
    # store all of video details from the request
    videoDatas = []

    if response.method == 'POST':
        searchUrl = 'https://www.googleapis.com/youtube/v3/search'
        searchParameter = {
            'part': 'snippet',
            # search query is the search input value
            'q': response.POST['search'],
            'maxResults': 18,
            'type': 'video',
            'key': settings.YOUTUBE_DATA_API_KEY
        }
        r = requests.get(searchUrl, params=searchParameter).json()
        results = r['items']

        # store all of video ids from the request
        videoIds = []
        for result in results:
            videoIds.append(result['id']['videoId'])

        # search video with video ids we get above and other parameters
        videoUrl = 'https://www.googleapis.com/youtube/v3/videos'
        videoParameter = {
            'part': 'snippet, contentDetails',
            'id': ','.join(videoIds),
            'key': settings.YOUTUBE_DATA_API_KEY
        }
        r = requests.get(videoUrl, params=videoParameter).json()
        results = r['items']

        for result in results:
            videoData = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'duration': parse_duration(result['contentDetails']['duration']),
                'thumbnails': result['snippet']['thumbnails']['high']['url'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}'
            }
            videoDatas.append(videoData)

    # all of video data we are going to render on cards
    context = {'videoDatas': videoDatas}

    # send context into html
    return render(response, 'search/index.html', context)
