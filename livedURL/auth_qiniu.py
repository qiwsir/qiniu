#! /usr/bin/env python
#coding:utf-8

import datetime
import urllib
import hmac
from hashlib import sha1

import random
import string

import os
import json

class SafetyInterface():
    #url is a complete url, as: http://www.itdiffer.com/python/tornado?q=qiwei
    #ak is Access Key
    #sk is Secret Key
    def __init__(self, url, ak="", sk=""):
        self.url = url
        self.ak = ak
        self.sk = sk

    def splitUrl(self):  #url is a complete url, as: http://www.itdiffer.com/python/tornado?q=qiwei
        result = {}
    
        proto, rest = urllib.splittype(self.url)
        result['proto'] = proto
        host, rest = urllib.splithost(rest)
        result['host'] = host
        path, query = urllib.splitquery(rest)
        result['path'] = path
        result['query'] = query

        return result

    def interfaceAuth(self):
        result_dict = self.splitUrl()
        path = result_dict['path']
        query = result_dict['query']
        url_str = path + "?" + query + "\n"
        hashed = hmac.new(self.sk, url_str, sha1)
        return hashed.digest().encode("base64")

    def pushAuth(self, push_url): #push_url is : rtmp://115.238.155.183:49166/livestream/4q5cdgn2
        nonce = str(datetime.datetime.today())
        url = push_url + "?nonce=" + nonce
        stream_key =''.join(random.choice(string.lowercase) for i in range(10))
        hashed = hmac.new(stream_key, url, sha1)
        push_token = hashed.digest().encode("base64")
        url = url + "&token=" + push_token
        return url


class MangeStream():
    def __init__(self, ak, encoded_sign):
        self.ak = ak
        self.encoded_sign = encoded_sign

    def createStream(self):
        curl_str = "'http://api.pili.qiniu.com/v1/streams' "
        curl_str += "-H \'Authorization:pill " + self.ak +":" + self.encoded_sign +"\'"
        curl_str += " -H 'Content-Type: application/json' "
        curl_str += "-X POST --data-binary "

        stream_key =''.join(random.choice(string.lowercase) for i in range(10))

        data_dict = {}  
        data_dict['key'] = stream_key
        data_dict['is_private'] = False
        data_dict['comment'] = "custom comment"

        data_bin = json.dumps(data_dict)

        curl_str += "'" + data_bin + "'"
        
        command_str = "curl " + curl_str
        
        print command_str

        f = os.popen(command_str)
        return_str = f.read()

        return return_str

if __name__=="__main__":
    #access_key = "IC-juwKCoLkEZbevbA_QygH_z_-3XqoYqzKRJmfKxRo="
    #secret_key = "dCU-94bAXt0jQ4syMLVQ3zzmstA5Sydj1B_1hspIlJxhazX3kxmLQQAmSBHqJJ1rcS4pcEHJwCGS6uGvnycQIg=="
    access_key = "Rc7z9sbtDgpDKGGxbHP7mT4mffOLr8sIOSMbKt74"
    secret_key = "6wur2AO5prMdkudMz9CPz-7ncBrHW1qFXFJsfBh2"
    we_url = "rtmfp://zb.xilaixiwang.com:1910/meeting/38?userID=2083&userName=t1&classID=38&authority=teacher"
    safetyi = SafetyInterface(we_url, ak=access_key, sk=secret_key)
    encoded_sign = safetyi.interfaceAuth()
    manages = MangeStream(access_key, encoded_sign)
    print manages.createStream()


