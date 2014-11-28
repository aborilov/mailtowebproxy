#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
import urllib2
from google.appengine.api import mail

FROM = "aborilov@gmail.com"


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!!!')

    def post(self):
        message = mail.InboundEmailMessage(self.request.body)
        sender = message.sender
        url = message.subject
        try:
            result = urllib2.urlopen(url)
            page = result.read()
            out_message = mail.EmailMessage(
                sender=FROM, subject='RE: {}'.format(message.subject))
            out_message.to = message.sender
            out_message.body = page
            out_message.html = page
            out_message.send()
        except urllib2.URLError, e:
            logging.exception(e)
        self.response.write('ok')
app = webapp2.WSGIApplication([
    ('/.+', MainHandler)
], debug=True)
