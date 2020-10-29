<?php
/******************************************************************************
 * Copyright 2020 NAVER Corp.                                                 *
 *                                                                            *
 * Licensed under the Apache License, Version 2.0 (the "License");            *
 * you may not use this file except in compliance with the License.           *
 * You may obtain a copy of the License at                                    *
 *                                                                            *
 *     http://www.apache.org/licenses/LICENSE-2.0                             *
 *                                                                            *
 * Unless required by applicable law or agreed to in writing, software        *
 * distributed under the License is distributed on an "AS IS" BASIS,          *
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   *
 * See the License for the specific language governing permissions and        *
 * limitations under the License.                                             *
 ******************************************************************************/
namespace Plugins\AutoGen\GuzzleHttp;

use Plugins\Common\Candy;
use Plugins\Sys\curl\CurlUtil;


/**
 *@hook:GuzzleHttp\ClientTrait::get
 *@hook:GuzzleHttp\ClientTrait::post
 *@hook:GuzzleHttp\ClientTrait::patch
 */
class GuzzlePlugin extends Candy
{
    function onBefore()
    {
        pinpoint_add_clue(PP_DESTINATION,CurlUtil::getHostFromURL($this->args[0]));
        pinpoint_add_clues(PP_HTTP_URL,$this->args[0]);
        pinpoint_add_clue(PP_SERVER_TYPE,PP_PHP_REMOTE);

        $n_headers =[] ;
        if( is_array($this->args[1]) && array_key_exists('headers',$this->args[1]))
        {
            $n_headers = $this->args[1]['headers'];
        }
        $n_headers = array_merge($n_headers,CurlUtil::getPinpointHeader($this->args[0]));
        $this->args[1]['headers'] = $n_headers;
    }

    function onEnd(&$ret)
    {
//        $ret->getStatusCode();
        pinpoint_add_clues(PP_HTTP_STATUS_CODE,(string)($ret->getStatusCode()));
    }

    function onException($e)
    {
        pinpoint_add_clue(PP_ADD_EXCEPTION,$e->getMessage());
    }


}