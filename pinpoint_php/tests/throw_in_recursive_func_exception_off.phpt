--TEST--
Test pinpoint
--INI--
pinpoint_agent.pinpoint_enable=true
pinpoint_agent.trace_exception=false
profiler.proxy.http.header.enable=true
pinpoint_agent.unittest=true

--FILE--
<?php

class QuickStartPlugin extends \Pinpoint\Plugin
{
    public function __construct()
    {
        parent::__construct();
        $this->addSimpleInterceptor("test_cumsum_e1", -1);
    }
}

$p = new QuickStartPlugin();
pinpoint_add_plugin($p, basename(__FILE__, '.php'));
pinpint_aop_reload();


function test_cumsum_e1($n)
{
    if ($n < 1) throw new Exception("n < 1");
    $tmp = $n + test_cumsum_e1($n-1);
}
echo test_cumsum_e1(3);

?>
--EXPECTF--
request start
  addSimpleInterceptor name:[test_cumsum_e1]
  call test_cumsum_e1's interceptorPtr::onBefore
    SimpleInterceptor->addAnnotation key:[-1] value:[{[0]:3 }] 
  call test_cumsum_e1's interceptorPtr::onBefore
    SimpleInterceptor->addAnnotation key:[-1] value:[{[0]:2 }] 
  call test_cumsum_e1's interceptorPtr::onBefore
    SimpleInterceptor->addAnnotation key:[-1] value:[{[0]:1 }] 
  call test_cumsum_e1's interceptorPtr::onBefore
    SimpleInterceptor->addAnnotation key:[-1] value:[{[0]:0 }] 
  call test_cumsum_e1's interceptorPtr::onEnd
  call test_cumsum_e1's interceptorPtr::onEnd
  call test_cumsum_e1's interceptorPtr::onEnd
  call test_cumsum_e1's interceptorPtr::onEnd

Fatal error: Uncaught Exception: n < 1 in %s:%d
Stack trace:
#0 %s(20): test_cumsum_e1(0)
#1 %s(20): test_cumsum_e1(1)
#2 %s(20): test_cumsum_e1(2)
#3 %s(22): test_cumsum_e1(3)
#4 {main}
  thrown in %s on line %d
request shutdown