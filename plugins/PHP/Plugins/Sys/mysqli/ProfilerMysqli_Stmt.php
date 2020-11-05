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

/*
 * User: eeliu
 * Date: 11/5/20
 * Time: 5:32 PM
 */

namespace Plugins\Sys\mysqli;


class ProfilerMysqli_Stmt
{
    protected $_instance;
    public function __construct(&$instance)
    {
        $this->_instance = &$instance;
    }

    public function __call($name, $arguments)
    {
        return call_user_func_array([&$this->_instance,$name],$arguments);
    }

    public function bind_param ($types, &$var1, &...$_)
    {
        $param = \pinpoint_get_func_ref_args();
        return call_user_func_array([$this->_instance,'bind_param'],$param);

    }

    public function bind_result (&$var1, &...$_)
    {
        $param = \pinpoint_get_func_ref_args();
        return call_user_func_array([$this->_instance,'bind_result'],$param);
    }

    public function execute()
    {
        $plugin = new StmtExecutePlugin("Stmt::execute",$this);
        try{
            $plugin->onBefore();
            $ret =  call_user_func_array([$this->_instance,'execute'],[]);
            $plugin->onEnd($ret);
            return $ret;

        }catch (\Exception $e)
        {
            $plugin->onException($e);
        }
    }


}