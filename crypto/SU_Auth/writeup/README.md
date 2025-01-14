```python
if any(priv[i] == SUKEY[i] for i in range(len(ells))) and LIMIT: return "🙅SUKEY"
```

The incorrect use of the `any` function means that each entry of SUKEY can be recovered through a timing side channel attack. 

Since SUKEY cannot be used, the next step is to find an equivalent key for SUKEY.

Notice $\prod_{i=1}^r\mathfrak{l}_i=\overline{\mathfrak{l}}_0$ , where $\mathfrak{l_0}$ is the 4-isogeny, and the order is 3.

Combine this two, a helpful equation is $(\prod_{i=1}^r\mathfrak{l}_i)^3=[1]$ .

A easy equivalent key we have : )

```python
SUKEY_ = [i+3 for i in SUKEY]
```

