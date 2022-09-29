'''
    Description:
    Get information from Youtube in a simple way.

    Author: AlejandroV
    Version: 0.1.0
    Video: ?
'''
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import webbrowser

def render(url):
    ''' All process of getting information '''
    attempts = 0
    session = HTMLSession()
    
    print("Procesando...")
    while attempts < 3:
        try:
            r = session.get(url)
            r.html.render(sleep=1)
            break
        except:
            print('.')
            attempts += 1
            continue
    if attempts <= 3:
        return BeautifulSoup(r.html.html, "html.parser")
    else:
        return ''

def getChannelInfo(text):
    ''' Get channel information (name, subs and videos) '''
    text = text.replace(" ", "+")
    bs = render(f"https://www.youtube.com/results?search_query={text}&sp=EgIQAg%253D%253D")
    
    if bs != '':
        search = bs.select('div.style-scope.ytd-channel-renderer')[0]

        # channel name
        channel = search.select('yt-formatted-string.style-scope.ytd-channel-name')[0]

        # channel subscribers
        subs = search.select('span.style-scope.ytd-channel-renderer')[0]

        # channel videos
        videos = search.select('span.style-scope.ytd-channel-renderer')[2]
        
        return {'status': 200, 'name': channel.text, 'subs': subs.text.replace("M", "millones"), 'videos': videos.text}
    else:
        return {'status': 500, 'name': '', 'subs': '', 'videos': ''}

def play(text):
    ''' Open a youtube video '''
    text = text.replace(" ", "+")
    bs = render(f"https://www.youtube.com/results?search_query={text}")

    if bs != '':
        search = bs.select('a.yt-simple-endpoint.style-scope.ytd-video-renderer')[0]
        webbrowser.open("www.youtube.com" + search['href'])