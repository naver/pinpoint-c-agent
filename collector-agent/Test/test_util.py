


#!/usr/bin/env python
from unittest import TestCase

from CollectorAgent.TPackets import *


# -*- coding: UTF-8 -*-

from Span_pb2 import PAcceptEvent, PSpan, PSpanEvent
# !/usr/bin/env python
from unittest import TestCase

from CollectorAgent.TPackets import *
from Span_pb2 import PAcceptEvent, PSpan, PSpanEvent


# -*- coding: UTF-8 -*-


class TestUtil(TestCase):
    def test_parseNetByteStream(self):
        netFlow = struct.pack('!hii9shih',PacketType.CONTROL_HANDSHAKE,2,9,"123456789".encode(),PacketType.APPLICATION_STREAM_CLOSE,12345,0)
        view = memoryview(netFlow)

        ipacket =  Packet.parseNetByteStream(view,len(netFlow))

        tp = next(ipacket)


        self.assertEqual(tp[0], 19)
        self.assertEqual(tp[1],PacketType.CONTROL_HANDSHAKE)
        self.assertEqual(tp[2], 2)
        self.assertEqual(tp[3].tobytes(),"123456789".encode())

        tp = next(ipacket)


        self.assertEqual(tp[0], 27)
        self.assertEqual(tp[1],PacketType.APPLICATION_STREAM_CLOSE)
        self.assertEqual(tp[2],12345)
        self.assertEqual(tp[3],None)

    def test_queue(self):

        import threading
        from  queue import Queue
        simple_queue = Queue()

        def worker():
            times = 10000
            while times>0 :
                item = simple_queue.get()
                if item is None:
                    raise
                times-=1
                print("-1")

        def consumer():
            times = 10000
            while times > 0:
                simple_queue.put(consumer)
                times -= 1
                print("+1")


        producer = threading.Thread(target=worker)
        cons     = threading.Thread(target=consumer)
        producer.start()
        cons.start()
        producer.join()
        cons.join()
    def test_span(self):
        acceptEv = PAcceptEvent()
        args ={
            'acceptEvent':acceptEv
        }
        span = PSpan()
        span.serviceType =100
        print(span)

    def test_span_ev(self):
        spanEv = PSpanEvent()
        spanEv.depth = 1
        spanEv.sequence = 1
        print(spanEv)
