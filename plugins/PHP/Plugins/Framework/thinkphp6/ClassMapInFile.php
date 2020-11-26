<?php
#-------------------------------------------------------------------------------
# Copyright 2019 NAVER Corp
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.
#-------------------------------------------------------------------------------

namespace Plugins\Framework\thinkphp6;

use pinpoint\Common\AopClassMap;

class ClassMapInFile extends AopClassMap
{
    private $mustHoldClasses = ['Plugins\PerRequestPlugins' => null,"GuzzleHttp\ClientTrait"=>null,"GuzzleHttp\Proxied_ClientTrait"=>null];
    public function __construct()
    {
        parent::__construct();
    }

    public  function findFile($classFullName)
    {

        $file = parent::findFile($classFullName);
        if ($file) {
            if (!pinpoint_tracelimit()) {
                return $file;
            } elseif (array_key_exists($classFullName, $this->mustHoldClasses) == 1) {
                return $file;
            } else {
                 echo "reject $$classFullName <br>";
                return null;
            }
        }
        return $file;
    }
}
