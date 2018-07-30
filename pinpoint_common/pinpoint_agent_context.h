/*******************************************************************************
 * Copyright 2018 NAVER Corp.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License.  You may obtain a copy
 * of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
 * License for the specific language governing permissions and limitations under
 * the License.
 ******************************************************************************/
#ifndef PINPOINT_AGENT_CONTEXT_H
#define PINPOINT_AGENT_CONTEXT_H

#include <string>
#include <boost/shared_ptr.hpp>
#include "stdint.h"

namespace Pinpoint
{
    namespace Configuration
    {
        class Config;
    }

    namespace Agent
    {
        class PinpointAgentContext;
        typedef boost::shared_ptr<PinpointAgentContext> PinpointAgentContextPtr;

        struct AgentConfigArgs
        {
            std::string agentId;
            std::string applicationName;
            std::string collectorSpanIp;
            uint32_t collectorSpanPort;
            std::string collectorStatIp;
            uint32_t collectorStatPort;
            std::string collectorTcpIp;
            uint32_t collectorTcpPort;
            std::string logFileRootPath;
            std::string logLevel;
            uint32_t reconInterval;

            bool pluginIncludeIsSet;
            bool pluginExcludeIsSet;
            std::string pluginInclude;
            std::string pluginExclude;

            bool apiAssignFileNameIsSet;
            std::string apiAssignFileName;

            int32_t traceLimit;
            int32_t skipTraceTime;

            // #64
            std::string pluginFileName;
            std::string pluginDir;

            bool assignArgs(Configuration::Config*);

        };
        typedef boost::shared_ptr<AgentConfigArgs> AgentConfigArgsPtr;

        class PinpointAgentContext
        {
        public:
            std::string hostname;
            std::string ip;
            std::string ports;
            std::string agentId;
            std::string applicationName;
            int16_t serviceType;
            uint32_t mainProcessPid;
            std::string agentVersion;
            uint64_t startTimestamp;
            AgentConfigArgsPtr agentConfigArgsPtr;

            static int32_t initContext();
            static PinpointAgentContextPtr& getContextPtr();
        private:
            static PinpointAgentContextPtr instance;
        };
    }
}

#endif
