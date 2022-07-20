import requests


class AuthService:
    def __init__(self):
        super().__init__()
        self.url = None

    def get_token(self, consumer_key, consumer_secret):
        """
          Get the authentication token
        """
        oauth_token = None
        oauth_token_secret = None
        oauth_callback_confirmed = None
        url = 'https://api.twitter.com/oauth/request_token'
        cookies = {
            'guest_id': 'v1%3A165680799928951080',
        }
        headers = {
            'Cookie': 'guest_id=v1%3A165680799928951080',
        }
        params = {
            'oauth_consumer_key': consumer_key,
            'oauth_consumer_secret': consumer_secret,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': '1656808051',
            'oauth_nonce': 'nNXGP42Z3kg',
            'oauth_version': '1.0',
            'oauth_signature': 'cyWpYvrIsQse4mk8DYo9zUCobXk=',
        }
        try:
            resp = requests.post(url=url,
                                 params=params,
                                 cookies=cookies,
                                 headers=headers)
            if resp and resp.status_code == 200:
                oauth_token = resp.text.split('&')[0].split('=')[1]
                oauth_token_secret = resp.text.split('&')[1].split('=')[1]
                oauth_callback_confirmed = resp.text.split('&')[2].split('=')[1]
            else:
                raise Exception(f"Fail to authenticate on Twitter API: {resp.text}")
        finally:
            return oauth_token, oauth_token_secret, oauth_callback_confirmed

