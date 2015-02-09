#!/usr/bin/env python
# coding=utf-8

import tornado.web
import json

from db.db import *
from pilisdk.application import Application

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class CreateStream(tornado.web.RequestHandler):
    def post(self):
        class_id = int(self.get_argument("class_id"))
        
        if select_row(class_id):
            self.write("have been this class is.")
        else:
            access_key = "IC-juwKCoLkEZbevbA_QygH_z_-3XqoYqzKRJmfKxRo="
            secret_key = "dCU-94bAXt0jQ4syMLVQ3zzmstA5Sydj1B_1hspIlJxhazX3kxmLQQAmSBHqJJ1rcS4pcEHJwCGS6uGvnycQIg=="
            new_stream = Application(access_key, secret_key)
            
            push = new_stream.create_stream()
            push_stream = push.refresh()
            insert_stream(class_id, "push", json.dumps(push_stream))

            live = new_stream.create_stream()
            live_stream = live.refresh()
            insert_stream(class_id, "live", json.dumps(live_stream))
            self.write("have create the live stream.")


class GetStream(tornado.web.RequestHandler):
    def post(self):
        class_id = int(self.get_argument("class_id"))

        stream = select_row(class_id)
        return_values = [line for line in stream]
        print return_values
        self.write(json.dumps(return_values))
