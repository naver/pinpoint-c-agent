#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by eeliu at 10/21/19


# -*- coding: UTF-8 -*-
import time
import logging
from unittest import TestCase
from CollectorAgent.GrpcAgent import GrpcAgent
from CollectorAgent.GrpcMeta import GrpcMeta
from CollectorAgent.GrpcSpan import GrpcSpan
from Span_pb2 import PTransactionId, PSpan, PSpanMessage


class TestGRPCRoutine(TestCase):
    SEQ = 0
    def setUp(self) -> None:
        # import sys, os
        # sys.path.append(os.path.abspath('..'))
        # pass
        import sys
        logger= logging.getLogger()
        logger.level=logging.DEBUG
        console_handler=logging.StreamHandler(sys.stdout)
        logger.addHandler(console_handler)
        self.logger = logger
        starttime = str(int(time.time() * 1000))
        self.agent_meta = [('agentid', 'test-id'),
                      ('applicationname', 'test-name'),
                      ('starttime', starttime)]
        self.agent = GrpcAgent('dev-1230', '10.10.12.23', '2345', 4569, 'dev-pinpoint:9991', self.agent_meta)

    def _generate_span(self):

        tid = PTransactionId(agentId='test-id',agentStartTime=int(time.time()),sequence=TestGRPCRoutine.SEQ)
        span =PSpan(version = 1,
                    transactionId=tid,
                    startTime= int(time.time()),
                    elapsed=10,
                    apiId=1,
                    serviceType=1500,
                    applicationServiceType=1500)
        TestGRPCRoutine.SEQ+= 1
        msg= PSpanMessage(span=span)
        self.logger.debug("generator a span")
        return msg

    def test_sendspan(self):
        spanclient = GrpcSpan(self._generate_span, 'dev-pinpoint:9993', self.agent_meta, 10)
        time.sleep(5)

    def test_metaData(self):
        apis=(['aa',10,0],['ada',12,0],['aa',31,2],['aaf',11,3])
        strings = ('aaaaaaaaaaaa','bbbbbbbbbbb','cccccccc')
        sqls=('ssss','bbbbb','ssssssss')
        meta_client = GrpcMeta('dev-pinpoint:9991', self.agent_meta)
        id = 0
        for api in apis:
            id = meta_client.updateApiMeta(*api)
        self.assertEqual(id,3)
        for string in strings:
            id = meta_client.updateStringMeta(string)
        self.assertEqual(id, 6)
        for sql in sqls:
            id = meta_client.updateSqlMeta(sql)
        self.assertEqual(id, 9)

        id = meta_client.updateSqlMeta('ssss')
        self.assertEqual(id, 7)

        id = meta_client.updateStringMeta('bbbbbbbbbbb')
        self.assertEqual(id, 5)

        time.sleep(3)