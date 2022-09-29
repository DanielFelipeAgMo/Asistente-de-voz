#!/usr/bin/env python

import requests


class Track:

    deezer = None

    id_ = None
    title = None
    duration = None
    release_date = None
    album_id = None
    album_name = None
    artist_id = None

    def __init__(self, deezer, id, title, duration, release_date=None, album_id=None, album_title=None, **kwargs):
        """
        Create a Track
        :param Deezer deezer: obj to make other requests
        :param str id:
        :param str title:
        :param int duration:
        :param date release_date:
        :param str album_id:
        :param str album_title:
        :param kwargs: other params (see Deezer's documentation : https://developers.deezer.com/api/track)
        """

        self.deezer = deezer

        self.id_ = id
        self.title = title
        self.duration = duration
        self.release_date = release_date
        self.album_title = None
        self.album_id = album_id
        self.album_title = album_title
        self.artist_id = None

        if 'album' in kwargs:
            if 'id' in kwargs['album']:
                self.album_id = kwargs['album']['id']
            if 'title' in kwargs['album']:
                self.album_title = kwargs['album']['title']

        if 'artist' in kwargs:
            if 'id' in kwargs['artist']:
                self.artist_id = kwargs['artist']['id']

    def get_album(self):
        """
        Call API to get the album
        :rtype: Album
        """
        response = self.deezer.req_get(uri=f'/album/{self.album_id}')
        return Album(deezer=self.deezer, **response)

    def get_artist(self):
        """
        Call API to get the artist
        :rtype: Artist
        """
        response = self.deezer.req_get(uri=f'/artist/{self.artist_id}')
        return Artist(deezer=self.deezer, **response)


class Album:

    deezer = None

    id_ = None
    title = None
    nb_tracks = None
    cover = None
    track_ids = None

    def __init__(self, deezer, id, title, nb_tracks, cover, tracks, artist, **kwargs):
        """
        Create a Track
        :param Deezer deezer: obj to make other requests
        :param str id:
        :param str title:
        :param str cover:
        :param dict tracks: dict with information on the tracks
        :param dict artist: dict with information on the artist
        :param kwargs: other params (see Deezer's documentation : https://developers.deezer.com/api/album)
        """

        self.deezer = deezer

        self.id_ = id
        self.title = title
        self.nb_tracks = nb_tracks
        self.cover = cover
        self.artist_id = None

        self.track_ids = []
        for track_obj in tracks['data']:
            self.track_ids.append(track_obj['id'])

        if 'id' in artist:
            self.artist_id = artist['id']

    def get_tracks(self):
        """
        Call API to get the tracks of this album
        :rtype: List of Track
        """
        response = self.deezer.req_get(uri=f'/album/{self.id_}/tracks')

        tracks = []
        for row in response.get('data'):
            tracks.append(Track(deezer=self.deezer, album_id=self.id_, album_title=self.title, **row))

        return tracks

    def get_artist(self):
        """
        Call API to get the artist of this album
        :rtype: Artist
        """
        response = self.deezer.req_get(uri=f'/artist/{self.artist_id}')
        return Artist(deezer=self.deezer, **response)


class Playlist:

    deezer = None

    id_ = None
    title = None
    picture = None
    is_loved_track = None

    def __init__(self, deezer, id, title, picture, is_loved_track, **kwargs):
        """
        Create a Playlist
        :param Deezer deezer: obj to make other requests
        :param str id:
        :param str title:
        :param str picture:
        :param boolean is_loved_track:
        :param kwargs: other params (see Deezer's documentation : https://developers.deezer.com/api/playlist)
        """
        self.deezer = deezer

        self.id_ = id
        self.title = title
        self.picture = picture
        self.is_loved_track = is_loved_track


class Artist:

    deezer = None

    id_ = None
    name = None
    picture = None
    tracklist_url = None

    def __init__(self, deezer, id, name, picture, tracklist, **kwargs):
        """
        Create an Artist object
        :param Deezer deezer: obj to make other requests
        :param str id:
        :param str name:
        :param str picture: url of the artist picture
        :param tracklist: API Link to the top of this artist
        :param kwargs: other params (see Deezer's documentation : https://developers.deezer.com/api/artist)
        """
        self.deezer = deezer

        self.id_ = id
        self.name = name
        self.picture = picture
        self.tracklist_url = tracklist

    def get_tracks(self):
        """
        get artist track list
        :rtype: List of Track
        """
        response = self.deezer.req_get(url=self.tracklist_url)

        tracks = []
        for row in response.get('data'):
            tracks.append(Track(deezer=self.deezer, **row))

        return tracks


class Deezer:

    app_id = None
    access_token = None

    user_id = None
    tracklist = None

    def __init__(self, app_id, token):
        """
        :param str app_id:
        :param str token:
        """
        self.app_id = app_id
        self.access_token = token

    @staticmethod
    def get_oauth_login_url(app_id, redirect_uri):
        """
        get the url for the deezer login
        :param str app_id: your app id
        :param str redirect_uri: your redirect uri
        :return:
        :rtype: str
        """
        return f'https://connect.deezer.com/oauth/auth.php?app_id={app_id}&redirect_uri={redirect_uri}&perms=basic_access,email'

    @staticmethod
    def get_oauth_token(app_id, app_secret, code):
        """
        get the oauth token to use the API
        :param str app_id:
        :param str app_secret:
        :param str code:
        :rtype: str
        """
        url = f'https://connect.deezer.com/oauth/access_token.php?app_id={app_id}&secret={app_secret}&code={code}&output=json'
        response = requests.get(url)
        if response.text == 'wrong code':
            return 'wrong code'
        else:
            response = response.json()
            return response['access_token']

    def req_get(self, url=None, uri=None,):
        """
        Perform a GET request
        :param str url:
        :param str uri: partial url
        :return: json response
        """
        if uri:
            url = f'https://api.deezer.com{uri}'
        response = requests.get(url, {'access_token': self.access_token})
        if response is not None:
            return response.json()

    def get_flow(self):
        """
        Get use flow (list of tracks
        :rtype: list of Track
        """
        response = self.req_get(uri='/user/me/flow')

        tracks = []
        for row in response.get('data'):
            tracks.append(Track(deezer=self, **row))

        return tracks

    def get_my_playlists(self):
        """
        Get my playlists
        :rtype: list of Playlist
        """
        response = self.req_get(uri='/user/me/playlists')

        playlists = []
        for row in response.get('data'):
            playlists.append(Playlist(deezer=self, **row))

        return playlists

    def get_my_favorite_artists(self):
        """
        Get the list of my favorites artists
        :rtype: List of Artist
        """
        all_loaded = False
        artists = []
        url = None

        while not all_loaded:
            if url is None:
                response = self.req_get(uri=f'/user/me/artists')
            else:
                response = self.req_get(url=url)

            for row in response.get('data'):
                artists.append(Artist(deezer=self, **row))

            if response.get('next'):
                url = response['next']
            else:
                all_loaded = True

        return artists

    def get_artist(self, artist_id):
        """
        Get an artist from his ID
        :param artist_id:
        :return: return an Artist
        :rtype: Artist
        """
        response = self.req_get(uri=f'/artist/{artist_id}')
        return Artist(deezer=self, **response)

    def get_widget(self, tracks=None, playlist=None, width=700, height=400):
        """
        Play a list of tracks or a playlist
        :param List[Track] tracks:
        :param Playlist playlist:
        :param number width: width of the widget
        :param number height: height of the widget
        """
        ids = None
        type_ = None

        if tracks is not None:
            ids = []
            for track in tracks:
                ids.append(track.id_)
            type_ = 'tracks'
        elif playlist is not None:
            ids = playlist.id_
            type_ = 'playlist'

        url = f'https://www.deezer.com/plugins/player?' \
              f'app_id={self.app_id}' \
              '&format=classic' \
              '&autoplay=true' \
              '&playlist=true' \
              f'&width={width}&height={height}&color=ff0000' \
              '&layout=dark' \
              '&size=medium' \
              f'&type={type_}' \
              f'&id={ids}' \
              '&popup=true' \
              '&repeat=' \
              '0&current_song_index=0' \
              '&current_song_time=2' \
              '&playing=true'

        return url