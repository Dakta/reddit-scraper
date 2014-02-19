import httplib2
import simplejson as json
import time
import urllib


class SpiderBase(object):

    def __init__(self, username=None, password=None):        
        # init
        self.username = username
        self.password = password
        self.http = httplib2.Http()
        self.max_attempts = 3
        self.attempts = 0

    def _login(self):
        headers = {}
        if self.username and self.password:
            url = 'http://www.reddit.com/api/login/' + self.username   
            body = {'user': self.username, 'passwd': self.password}
            headers = {'Content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'reddit comment scraper operated by /u/dakta'}
            response, content = self.http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
            headers = {'Cookie': response['set-cookie']}
        return headers

    def _get_json(self, uri):
        self.attempts = 0
        try:
            response, content = self.http.request(uri, 'GET', headers=self._login())
        except httplib2.ServerNotFoundError, e:
            self._recurse(uri)
        
        if response['status'] == '200':
            out = json.loads(content)
            if out is None:
                self._recurse(uri)
            return out
        else:
            self._recurse(uri)

    def _recurse(uri):
        self.attempts = self.attempts + 1

        if attempts <= self.max_attempts:
            self._get_json(uri)
        else:
            # error handling?
            pass
