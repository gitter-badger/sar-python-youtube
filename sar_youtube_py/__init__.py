"""
    The MIT License (MIT)

    Copyright (c) 2014 Sardorbek Pulatov <sardorbek_pulatov@fastmail.fm> <sardorbek.pulatov@outlook.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""
__author__ = 'Sardorbek Pulatov'
import urllib
import requests
import json


class SarYouTube:
    def __init__(self, **kwargs):
        self.scope = 'https://www.googleapis.com/auth/youtube.readonly'  # Default Scope
        self.api_url = 'https://www.googleapis.com/youtube/v3'  # API endpoint
        self.auth_url = 'https://accounts.google.com/o/oauth2/auth?'  # Auth Url
        self.token_url = 'https://accounts.google.com/o/oauth2/token'  # Token URL

        self.access_type = 'offline'
        self.response_type = 'code'

        self.__dict__.update(kwargs)

    def get_login_url(self, **kwargs):
        self.__dict__.update(kwargs)
        auth_params = {
            'client_id': self.client_id,
            'scope': self.scope,
            'redirect_uri': self.redirect_uri,
            'access_type': self.access_type,
            'response_type': self.response_type,
        }

        return self.auth_url + urllib.urlencode(auth_params)

    def set_auth_token(self, auth_token):
        self.auth_token = auth_token

    def set_refresh_token(self, refresh_token):
        self.refresh_token = refresh_token

    def set_access_token(self, access_token):
        self.access_token = access_token

    def get_refresh_token(self, refresh_token):
        return self.refresh_token

    def get_access_token(self, refresh=False):
        """
            Returns dict with

            "access_token"
            "token_type"
            "expires_in"
            "refresh_token" - if access_type set as offline
        """
        data = {
            'code': self.auth_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }

        request = requests.post(self.token_url, data)

        return self.check_request(request)

    def api(self, api_path, **kwargs):
        """
            Makes API request to the YouTube
            If type is set as post, then makes post request

            api_path api name to call (ex /channels )
        """
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

        if 'type' in kwargs and kwargs['type'] == 'post':
            request = requests.post(self.api_url + api_path, kwargs, headers=headers)
        else:
            request = requests.get(self.api_url + api_path + '?' + urllib.urlencode(kwargs), headers=headers)

        response = json.loads(request.content)
        if 'error' in response and response['error'] == 'invalid_grant' and self.refresh_token:
            self.refresh_token()
            return self.api(api_path, kwargs)

        return self.check_request(request)

    def refresh_access_token(self, refresh_token):
        data = {
            'refresh_token': self.auth_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        }

        request = requests.post(self.token_url, data)

        return self.check_request(request)

    def check_request(self, request):
        """
            Checks for status code, is status code is other than 200, throws an exception
        """
        if request.status_code != 200:
            response = json.loads(request.content)
            raise Exception('Request is not successful, status code : ' + str(request.status_code) + ', Error : ' +
                            response['error'])
        else:
            json_object = request.json()
            if 'refresh_token' in json_object:
                self.set_access_token(json_object['refresh_token'])

            return json_object