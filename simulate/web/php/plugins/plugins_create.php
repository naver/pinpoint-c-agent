<?php
/**
 * Copyright 2018 NAVER Corp.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

$path=dirname(__FILE__);
foreach (glob($path ."/*plugin.php") as  $value) {
    include_once($value);
    echo $value. "\n";
}

$p = new QuickStartPlugin();
pinpoint_add_plugin($p, "quickstart_plugin.php");

$p = new ExcludePlugin();
pinpoint_add_plugin($p, "exclude_plugin.php");

$p = new CurlPlugin();
pinpoint_add_plugin($p, "curl_plugin.php");

$p =new TestPlugin();
pinpoint_add_plugin($p, "test_plugin.php");

$p =new TestPlugin01();
pinpoint_add_plugin($p, "test_01_plugin.php");

$p = new Issue200Plugin();
pinpoint_add_plugin($p, "issue200_plugin.php");

$p =  new WorkerManPlugins();
pinpoint_add_plugin($p,"workerman_plugin.php");

pinpint_aop_reload();

?>