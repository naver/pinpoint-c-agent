#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ------------------------------------------------------------------------------
#  Copyright  2020. NAVER Corp.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ------------------------------------------------------------------------------

# Created by eeliu at 11/5/19
import Service_pb2_grpc
from CollectorAgent.GrpcClient import GrpcClient
from Common.Logger import TCLogger
from Span_pb2 import PSqlMetaData, PApiMetaData, PStringMetaData
from Events.GTimer import GTimer

class GrpcMeta(GrpcClient):
    def __init__(self, address, meta=None):
        super().__init__(address, meta, -1)
        self.meta_stub = Service_pb2_grpc.MetadataStub(self.channel)
        self.must_snd_meta_now = False
        self.id = 0
        self.sql_table = {}
        self.api_table = {}
        self.string_table = {}
        self.recover_timer = GTimer()

    def _sendSqlMeta(self, meta):
        assert isinstance(meta, PSqlMetaData)
        future = self.meta_stub.RequestSqlMetaData.future(meta)
        future.add_done_callback(self._response)

    def _sendApiMeta(self, meta):
        assert isinstance(meta, PApiMetaData)
        future = self.meta_stub.RequestApiMetaData.future(meta)
        future.add_done_callback(self._response)

    def _sendStringMeta(self, meta):
        assert isinstance(meta, PStringMetaData)
        future = self.meta_stub.RequestStringMetaData.future(meta)
        future.add_done_callback(self._response)

    def _channelCheck(fun):
        def update(self, *args):
            if self.must_snd_meta_now:
                self.recover_timer.start(self._registerAllMeta, 10)
            result = fun(self, *args)
            return result
        return update

    @_channelCheck
    def updateApiMeta(self, apiInfo, line, type):
        row_str = ("%s-%d-%d" % (apiInfo, line, type))
        if row_str in self.api_table:
            return self.api_table[row_str][0]
        else:
            id = self.id
            meta = PApiMetaData(apiId=id, apiInfo=apiInfo, line=line, type=type)
            self.api_table[row_str] = [id, meta]
            self._sendApiMeta(meta)
            self.id += 1
            TCLogger.debug("register api meta id:%d -> api:[%s]", id, row_str)
            return id
            
    @_channelCheck
    def updateStringMeta(self, value):
        if value in self.string_table:
            return self.string_table[value][0]
        else:
            id = self.id
            meta = PStringMetaData(stringId=id, stringValue=value)
            self.string_table[value] = [id, meta]
            self._sendStringMeta(meta)
            self.id += 1
            TCLogger.debug("register string meta id:%d -> value:[%s]", id, value)
            return id

    @_channelCheck
    def updateSqlMeta(self, sql):
        if sql in self.sql_table:
            return self.sql_table[sql][0]
        else:
            id = self.id
            meta = PSqlMetaData(sqlId=id, sql=sql)
            self.sql_table[sql] = [id, meta]
            self._sendSqlMeta(meta)
            self.id += 1
            TCLogger.debug("register sql meta id:%d -> sql:[%s]", id, sql)
            return id


    def _response(self, future):
        if future.exception():
            TCLogger.warning("register meta failed %s", future.exception)
            # self.is_ok = False
            return
        self.must_snd_meta_now = False


    def channelSetReady(self):
        pass

    def channelSetIdle(self):
        self.must_snd_meta_now =True

    def channelSetError(self):
        self.must_snd_meta_now =True

    def _registerAllMeta(self):
        TCLogger.info("register all meta data")
        # register sql
        for key, value in self.sql_table.items():
            self._sendSqlMeta(value[1])
        # api
        for key, value in self.api_table.items():
            self._sendApiMeta(value[1])
        # string
        for key, value in self.string_table.items():
            self._sendStringMeta(value[1])

    def start(self):
        pass
