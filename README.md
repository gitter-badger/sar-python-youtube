Mini Python lib for YouTube Data API
==================

Easy to use :

```python
from sar_youtube_py import SarYouTube

youtube = SarYouTube(
        client_id='YOUR_CLIENT_ID',
        client_secret = 'CLIENT_SECRET',
        redirect_uri='http://localhost:5000/youtube_auth'
)


tokens = youtube.get_access_token()

youtube.set_access_token(tokens['access_token'])

answer = youtube.api('/channels', part='id,contentDetails', mine='true')
```