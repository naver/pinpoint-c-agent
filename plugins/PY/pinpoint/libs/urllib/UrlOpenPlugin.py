#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ------------------------------------------------------------------------------
#  Copyright  2020. NAVER Corp.                                                -
#                                                                              -
#  Licensed under the Apache License, Version 2.0 (the "License");             -
#  you may not use this file except in compliance with the License.            -
#  You may obtain a copy of the License at                                     -
#                                                                              -
#   http://www.apache.org/licenses/LICENSE-2.0                                 -
#                                                                              -
#  Unless required by applicable law or agreed to in writing, software         -
#  distributed under the License is distributed on an "AS IS" BASIS,           -
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    -
#  See the License for the specific language governing permissions and         -
#  limitations under the License.                                              -
# ------------------------------------------------------------------------------

# Created by eeliu at 8/20/20

from pinpoint.common import *
import pinpointPy

class UrlOpenPlugin(Candy):

    def __init__(self, name):
        super().__init__(name)
        self.dst = ''
        self.url =''
    def onBefore(self,*args, **kwargs):
        super().onBefore(*args, **kwargs)
        self.url = args[0]
        generatePinpointHeader(self.url,kwargs['headers'])
        ###############################################################
        pinpointPy.add_clue(PP_INTERCEPTER_NAME,self.getFuncUniqueName())
        pinpointPy.add_clue(PP_SERVER_TYPE,PP_METHOD_CALL)
        pinpointPy.add_clues(PP_ARGS, self.url)
        ###############################################################

        return args,kwargs

    def onEnd(self,ret):
        ###############################################################
        pinpointPy.add_clue(PP_DESTINATION, urlparse(self.url)['netloc'])
        pinpointPy.add_clue(PP_SERVER_TYPE, PP_REMOTE_METHOD)
        pinpointPy.add_clue(PP_NEXT_SPAN_ID, pinpointPy.get_context_key(PP_NEXT_SPAN_ID))
        pinpointPy.add_clues(PP_HTTP_URL, self.url)
        pinpointPy.add_clues(PP_HTTP_STATUS_CODE, str(ret.status_code))
        pinpointPy.add_clues(PP_RETURN, str(ret))
        ###############################################################
        super().onEnd(ret)
        return ret

    def onException(self, e):
        pinpointPy.add_clue(PP_ADD_EXCEPTION,str(e))

