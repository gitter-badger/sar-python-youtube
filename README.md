Mini Python lib for YouTube Data API
==================
[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/pROCKrammer/sar-python-youtube?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Easy to use :

```python
from sar_youtube_py import SarYouTube

youtube = SarYouTube(
        client_id='YOUR_CLIENT_ID',
        client_secret = 'CLIENT_SECRET',
        redirect_uri='http://localhost:5000/youtube_auth'
)




youtube.set_auth_token(request.values.get('code'))

tokens = youtube.get_access_token()

youtube.set_access_token(tokens['access_token'])

answer = youtube.api('/channels', part='id,contentDetails', mine='true')
```
