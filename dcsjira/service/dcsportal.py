import json
import logging
import urllib


class Dcsportal(object):

    def __init__(self, api_url, logger=logging.getLogger(__name__)):
        self.api_url = api_url
        self.logger = logger

    def get_group_detail(self, group_id):
        params = urllib.urlencode({'type': 'groupmember', 'format': 'jsonp', 'jsobj': 'JS_OBJ', 'groupid': group_id})
        res = urllib.urlopen(self.api_url, params)

        if res.code != 200:
            return None

        result = json.loads(res.read())

        if result['groupList']['return']['code'] != '001':
            return None

        members = result['groupList']['group'][0]['member']
        phones = {}

        for member in members:
            phones[member['phone'].replace(' ', '').replace('-', '')] = member['displayName']

        return phones
