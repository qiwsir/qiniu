#! /usr/bin/env python
#coding:utf-8

import datetime
import hmac, hashlib, base64
import requests
import random
import string

class SafetyInterface(object):
    #url is a complete url, as: http://www.itdiffer.com/python/tornado?q=qiwei
    #ak is Access Key
    #sk is Secret Key
    def __init__(self, path, query, ak="", sk=""):
        self.path = path
        self.query = query
        self.ak = ak
        self.sk = sk

    def interfaceAuth(self):
        url_str = self.path + "?" + self.query 
        hashed = hmac.new(self.sk, url_str, hashlib.sha1)
        encoded = base64.urlsafe_b64encode(hashed.digest())
        return 'pili {0}:{1}'.format(self.ak, encoded)

    def pushStreamAuth(self, push_url): #push_url is : rtmp://115.238.155.183:49166/livestream/4q5cdgn2
        nonce = str(datetime.datetime.today())
        url = push_url + "?nonce=" + nonce
        stream_key =''.join(random.choice(string.lowercase) for i in range(10))
        hashed = hmac.new(stream_key, url, hashlib.sha1)
        push_token = base64.urlsafe_b64encode(hashed.digest())
        url = url + "&token=" + push_token
        return url


def createStream(path, query, access_key, secret_key):
    headers = {'content-type': 'application/json'}
    authed = SafetyInterface(path, query, access_key, secret_key)
    headers['Authorization'] = authed.interfaceAuth()
    url = "http://api.pili.qiniu.com/v1/streams"
    r = requests.post(url, headers=headers)
    return r.text

def statusStream(stream_id, path, query, access_key, secret_key):
    headers = {'content-type': 'application/json'}
    authed = SafetyInterface(path, query, access_key, secret_key)
    headers['Authorization'] = authed.interfaceAuth()
    url = "http://api.pili.qiniu.com/v1/streams/" + stream_id + "/status"
    r = requests.get(url, params=headers)
    return r.text

def pushStream(push_url, path, query, access_key, secret_key):
    authed = SafetyInterface(path, query, access_key, secret_key)
    push_auth = authed.pushStreamAuth(push_url)
    return push_auth

def main():
    access_key = "IC-juwKCoLkEZbevbA_QygH_z_-3XqoYqzKRJmfKxRo="
    secret_key = "dCU-94bAXt0jQ4syMLVQ3zzmstA5Sydj1B_1hspIlJxhazX3kxmLQQAmSBHqJJ1rcS4pcEHJwCGS6uGvnycQIg=="
    path = '/meeting/38'
    query = 'classID=38'
    #stream = createStream(path, query, access_key, secret_key)
    #stream_id = "54cb3584edf2230008000001"
    #status_stream = statusStream(stream_id, path, query, access_key, secret_key)
    #print status_stream
    #print stream
    push_url = "rtmp://rtmp.pili.clouddn.com/livestream/l20ff95m"
    stream_url = pushStream(push_url, path, query, access_key, secret_key)
    print stream_url

if __name__=="__main__":
    main()

