The curve in question is the pair-friendly curve BLS12-381. For this challenge, our goal is to find G1 or G2. Because the flag is padded, the most significant bit of the flag character is 0. The corresponding curve points have this form：
$$
a*G_1+b*P_2
$$
We multiply this point by n2 and we get rid of P2 and we get n2G1.

 If we pair n2G1 with $x*G_1+y*P_2$, G1 cancels out again. And we get pairing result $e(y*P_2,n_2*G_1)=e(P_2,n_2*G_1)^y$

The y here should not affect the order, so we drop it and consider:
$$
e(P_2,n_2*G_1)=e(o/n_2*G_2,n_2*G_1)=e(G_1,G_2)^{o/n_2*n_2} = e(G_1,G_2)^o = 1
$$
From this conclusion, each bit of flag can be judged.