#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by eeliu at 12/29/20


# ******************************************************************************
#   Copyright  2020. NAVER Corp.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ******************************************************************************

from pinpoint.common import Interceptor


def monkey_patch():
    try:
        import celery
        from celery.app.task import Task
        from celery.result import AsyncResult

        from .TaskPlugin import TaskPlugin
        from .GetPlugin import GetPlugin

        Interceptors = [
            Interceptor(Task, 'delay', TaskPlugin),
            Interceptor(AsyncResult, 'get', GetPlugin),
        ]
        for interceptor in Interceptors:
            interceptor.enable()
    except ImportError as e:
        # do nothing
        print(e)

__all__=['monkey_patch']