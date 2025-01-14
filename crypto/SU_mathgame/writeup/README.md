Just a easy challenge. 
For game1, you need find a big carmichael number. You can google and find that:

![1](C:\Users\29741\Desktop\SUCTF-crypto\SU_mathgame\writeup\img\1.png)

So you can do this to get:

```
from Crypto.Util.number import *
import random

while True:
    k = getRandomNBitInteger(338)
    if isPrime(6*k+1) and isPrime(12*k+1) and isPrime(18*k+1):
        print(k)
        break
```

For game2, it is required to solve a specific condition of the Diophantine equation. You could actually solve it on an elliptic curve, and maybe there's another way to do it.

[link](https://zhuanlan.zhihu.com/p/33853851)

For game3, the test point is the complex ratio invariance of the Mobius transform, but the random numbers can be predicted due to an oversight. You can see how expected solution works in exp.

