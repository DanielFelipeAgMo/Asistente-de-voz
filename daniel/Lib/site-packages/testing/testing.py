from deezersdk import deezersdk

if __name__ == '__main__':

    DEEZER_APP_ID = "212002"
    DEEZER_APP_SECRET = "7ebfb425e984e0770a00e347626b51ca"
    deezer = deezersdk.Deezer(app_id=DEEZER_APP_ID,
                              app_secret=DEEZER_APP_SECRET,
                              code="fr30d25351529630db73d13e71e43dc3",
                              token='frfz2KLjxwOBLBPxmNz6AjTP6orMA2cZkN6jnc4NDtBWFLD1xp')

    artist = deezer.get_artist(1)
    tracks = artist.get_tracks()
    album = tracks[0].get_album()
    album_tracks = album.get_tracks()
