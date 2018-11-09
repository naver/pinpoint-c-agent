////////////////////////////////////////////////////////////////////////////////
// Copyright 2018 NAVER Corp.
// 
// Licensed under the Apache License, Version 2.0 (the "License"); you may not
// use this file except in compliance with the License.  You may obtain a copy
// of the License at
// 
//   http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
// License for the specific language governing permissions and limitations under
// the License.
////////////////////////////////////////////////////////////////////////////////
#include "interceptor.h"
#include "request_plugin.h"
#include "../php_common.h"

using namespace Pinpoint::log;
using namespace Pinpoint::Plugin;
using namespace Pinpoint::Trace;
using namespace Pinpoint::Agent;


//<editor-fold desc="PhpRequestInterceptor">

PhpRequestInterceptor::PhpRequestInterceptor(const std::string &interceptedFuncName,
                                             const PhpRequestPluginPtr &pluginPtr)
        : Pinpoint::Plugin::Interceptor(interceptedFuncName), state(E_STOP), pluginPtr(pluginPtr)
{
}


int32_t PhpRequestInterceptor::startTrace()
{
    HttpHeader* pHeader = RequestHeader::getCurrentRequestHeader();

    int32_t err = Trace::startTrace(pHeader);
    if (err == Pinpoint::SAMPLING_IGNORE)
    {
        PP_U_TRACE("This trace had ignored by TraceLimit");
        return Pinpoint::SAMPLING_IGNORE;
    }
    else if (err != SUCCESS)
    {
        LOGE("startTrace failed.");
        return Pinpoint::FAILED;
    }

    TracePtr tracePtr = Trace::getCurrentTrace();

    assert (pluginPtr != NULL);
    assert (tracePtr != NULL);

    tracePtr->setApiId(pluginPtr->getRequestApi());

    std::string endPoint = get_end_point();
    if (endPoint != "")
    {
        tracePtr->setEndPoint(endPoint);
    }

    std::string remoteAddr = get_remote_addr();
    if (remoteAddr != "")
    {
        tracePtr->setRemoteAddr(remoteAddr);
    }

    std::string rpc = get_rpc();
    if (rpc != "")
    {
        tracePtr->setRpc(rpc);
    }

    return SUCCESS;
}

int32_t PhpRequestInterceptor::endTrace()
{
    if (!Trace::isStarted())
    {
        return SUCCESS;
    }
    return Trace::endTrace();
}

int32_t PhpRequestInterceptor::init()
{
    LOGI("PhpRequestInterceptor::init() SUCCESS!");

    return SUCCESS;
}

void PhpRequestInterceptor::onBefore(uint64_t callId,
                                     Pinpoint::Plugin::FuncArgFetcher& argFetcher)
{
    (void)callId;
    switch (startTrace())
    {
        case Pinpoint::SAMPLING_IGNORE:
        case Pinpoint::FAILED:
        {
            state = E_STOP;
            return ;
        }
        break;
        case SUCCESS:
        {
            state = E_STARTED;
        }
        break;
        default:
        {
            state = E_STARTED;
        }
    }

    LOGI(" called %p %d ",this,state);

    // add proxy header checking
    if(!PINPOINT_G(proxy_headers))
    {
    	return ;
    }

    TracePtr tracePtr = Trace::getCurrentTrace();
    PINPOINT_ASSERT (tracePtr != NULL);


    /// add PROXY_HTTP_HEADER when request start
    /// avoiding error jmp, if that the end-callback could be jmp
    std::string proxyHeader="";

    AnnotationPtr annotationPtr = Annotation::createAnnotation(AnnotationKey::PROXY_HTTP_HEADER);
    int type = 0;
    if (annotationPtr != NULL && get_proxy_http_header(proxyHeader,type))
    {
        LOGD("proxy_header %s",proxyHeader.c_str());

        annotationPtr->addTLongIntIntByteByteStringValue(proxyHeader,type);
        tracePtr->addAnnotationPtr(annotationPtr);
    }
}

void PhpRequestInterceptor::onEnd(uint64_t callId,
                                  Pinpoint::Plugin::FuncArgFetcher& argFetcher,
                                  Pinpoint::Plugin::FuncResultFetcher& resultFetcher)
{

    if( state != E_STARTED )
    {
        LOGW("phprequest interceptor no started");
        return;
    }

    (void)callId;

    TracePtr tracePtr = Trace::getCurrentTrace();
    PINPOINT_ASSERT (tracePtr != NULL);

    AnnotationPtr annotationPtr =
            Annotation::createAnnotation(AnnotationKey::HTTP_STATUS_CODE);
    if (annotationPtr != NULL)
    {
        annotationPtr->addIntValue(get_http_response_status());
        tracePtr->addAnnotationPtr(annotationPtr);
    }

    int32_t err = endTrace();

    if (err == Pinpoint::FAILED)
    {
        LOGE("endTrace failed.");
    }

    PP_U_TRACE("%s",err == Pinpoint::SAMPLING_IGNORE?("This trace had ignored by skiptracetime"):(""));

    state = E_STOP;

    return;
}

//</editor-fold>

//<editor-fold desc="PhpRequestPlugin">

PhpRequestPlugin::PhpRequestPlugin()
        : requestApiId(INVALID_API_ID)
{


}

int32_t PhpRequestPlugin::init()
{
    AgentPtr& agentPtr = Agent::getAgentPtr();
    assert (agentPtr != NULL);

    // 1, add api
    this->requestApiId = agentPtr->addApi("PHP Request", -1, Pinpoint::API_WEB_REQUEST);

  //   2, add string
//    this->exceptionStringId = agentPtr->addString("Exception");

    // 3, add interceptor
//    Pinpoint::Plugin::InterceptorPtr interceptorPtr;
//    try
//    {
//        interceptorPtr.reset(new PhpRequestInterceptor(PHP_REQUEST_FUNC_NAME, shared_from_this()));
//        // new and initialize it
//        interceptorPtr->init();
//    }
//    catch (std::bad_alloc&)
//    {
//        LOGE("create PhpRequestInterceptor failed.");
//        return Pinpoint::FAILED;
//    }

//    this->interceptors.push_back(interceptorPtr);


    Pinpoint::Plugin::InterceptorPtr interceptorPtr;
    interceptorPtr.reset(new PhpRequestInterceptor(PHP_REQUEST_FUNC_NAME, shared_from_this()));
    // new and initialize it
    interceptorPtr->init();
    PhpAop* aop = PhpAop::getInstance();
    assert (aop != NULL);
    aop->setRequestInterceptorPtr(interceptorPtr);


    return SUCCESS;
}

Pinpoint::Plugin::InterceptorPtrVector& PhpRequestPlugin::getAllInterceptors()
{
    return this->interceptors;
}

int32_t PhpRequestPlugin::getRequestApi()
{
    return this->requestApiId;
}


//</editor-fold>
