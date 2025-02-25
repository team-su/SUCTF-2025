Seems like a hidden number problem but pay attention to something in description:

<center>cyberC<font color=red>lier</font>:)</center>

Here lier actually implies that the total task is lying! Note that the task specifically gives the dockerfile to indicate that the version of sagemath is 10.5. We can look up the [documents](https://github.com/sagemath/sage/blob/develop/src/sage/rings/polynomial/polynomial_ring.py#L1389) and find that the implementation of `PR.random_element()` is as follows:

```python
def random_element(self, degree=(-1, 2), monic=False, *args, **kwds):
    r"""
    Return a random polynomial of given degree (bounds).

    INPUT:

    - ``degree`` -- (default: ``(-1, 2)``) integer for fixing the degree or
        a tuple of minimum and maximum degrees

    - ``monic`` -- boolean (default: ``False``); indicate whether the sampled
        polynomial should be monic

    - ``*args, **kwds`` -- additional keyword parameters passed on to the
        ``random_element`` method for the base ring

    EXAMPLES::

        sage: R.<x> = ZZ[]
        sage: f = R.random_element(10, x=5, y=10)
        sage: f.degree()
        10
        sage: f.parent() is R
        True
        sage: all(a in range(5, 10) for a in f.coefficients())
        True
        sage: R.random_element(6).degree()
        6

    If a tuple of two integers is given for the ``degree`` argument, a
    polynomial is chosen among all polynomials with degree between them. If
    the base ring can be sampled uniformly, then this method also samples
    uniformly::

        sage: R.random_element(degree=(0, 4)).degree() in range(0, 5)
        True
        sage: found = [False]*5
        sage: while not all(found):
        ....:     found[R.random_element(degree=(0, 4)).degree()] = True

    Note that the zero polynomial has degree `-1`, so if you want to
    consider it set the minimum degree to `-1`::

        sage: while R.random_element(degree=(-1,2), x=-1, y=1) != R.zero():
        ....:     pass

    Monic polynomials are chosen among all monic polynomials with degree
    between the given ``degree`` argument::

        sage: all(R.random_element(degree=(-1, 1), monic=True).is_monic() for _ in range(10^3))
        True
        sage: all(R.random_element(degree=(0, 1), monic=True).is_monic() for _ in range(10^3))
        True

    TESTS::

        sage: R.random_element(degree=[5])
        Traceback (most recent call last):
        ...
        ValueError: degree argument must be an integer or a tuple of 2 integers (min_degree, max_degree)

        sage: R.random_element(degree=(5,4))
        Traceback (most recent call last):
        ...
        ValueError: minimum degree must be less or equal than maximum degree

    Check that :issue:`16682` is fixed::

        sage: R = PolynomialRing(GF(2), 'z')
        sage: for _ in range(100):
        ....:     d = randint(-1, 20)
        ....:     P = R.random_element(degree=d)
        ....:     assert P.degree() == d

    In :issue:`37118`, ranges including integers below `-1` no longer raise
    an error::

        sage: R.random_element(degree=(-2, 3))  # random
        z^3 + z^2 + 1

    ::

        sage: 0 in [R.random_element(degree=(-1, 2), monic=True) for _ in range(500)]
        False

    Testing error handling::

        sage: R.random_element(degree=-5)
        Traceback (most recent call last):
        ...
        ValueError: degree (=-5) must be at least -1

        sage: R.random_element(degree=(-3, -2))
        Traceback (most recent call last):
        ...
        ValueError: maximum degree (=-2) must be at least -1

    Testing uniformity::

        sage: from collections import Counter
        sage: R = GF(3)["x"]
        sage: samples = [R.random_element(degree=(-1, 2)) for _ in range(27000)]    # long time
        sage: assert all(750 <= f <= 1250 for f in Counter(samples).values())       # long time

        sage: samples = [R.random_element(degree=(-1, 2), monic=True) for _ in range(13000)] # long time
        sage: assert all(750 <= f <= 1250 for f in Counter(samples).values())       # long time
    """
    R = self.base_ring()

    if isinstance(degree, (list, tuple)):
        if len(degree) != 2:
            raise ValueError("degree argument must be an integer or a tuple of 2 integers (min_degree, max_degree)")
        if degree[0] > degree[1]:
            raise ValueError("minimum degree must be less or equal than maximum degree")
        if degree[1] < -1:
            raise ValueError(f"maximum degree (={degree[1]}) must be at least -1")
    else:
        if degree < -1:
            raise ValueError(f"degree (={degree}) must be at least -1")
        degree = (degree, degree)

    if degree[0] <= -2:
        degree = (-1, degree[1])

    # If the coefficient range only contains 0, then
    # * if the degree range includes -1, return the zero polynomial,
    # * otherwise raise a value error
    if args == (0, 1):
        if degree[0] == -1:
            return self.zero()
        else:
            raise ValueError("No polynomial of degree >= 0 has all coefficients zero")

    if degree == (-1, -1):
        return self.zero()

    # If `monic` is set, zero should be ignored
    if degree[0] == -1 and monic:
        if degree[1] == -1:
            raise ValueError("the maximum degree of monic polynomials needs to be at least 0")
        if degree[1] == 0:
            return self.one()
        degree = (0, degree[1])

    # Pick random coefficients
    end = degree[1]
    if degree[0] == -1:
        return self([R.random_element(*args, **kwds) for _ in range(end + 1)])

    nonzero = False
    coefs = [None] * (end + 1)

    while not nonzero:
        # Pick leading coefficients, if `monic` is set it's handle here.
        if monic:
            for i in range(degree[1] - degree[0] + 1):
                coefs[end - i] = R.random_element(*args, **kwds)
                if not nonzero and not coefs[end - i].is_zero():
                    coefs[end - i] = R.one()
                    nonzero = True
        else:
            # Fast path
            for i in range(degree[1] - degree[0] + 1):
                coefs[end - i] = R.random_element(*args, **kwds)
                nonzero |= not coefs[end - i].is_zero()

    # Now we pick the remaining coefficients.
    for i in range(degree[1] - degree[0] + 1, degree[1] + 1):
        coefs[end - i] = R.random_element(*args, **kwds)

    return self(coefs)
```

It can be seen that the random polynomial generation of the polynomial ring is completely dependent on the random coefficient generation of its base ring, and under `Zmod(2^128-2)`, the random number generation is based on the implementation of `randrange(0,2^128-2)` in Python based on MT19937, which can be said to be basically equivalent to `getrandbits(128)`.

Back to the topic, since the polynomial ring is modulo $2^{128}-2$, it has a common factor of 2 with $2^{8}$, so it can be reduced to modulo 2. And now we will find that the core leakage content of each encryption is:
$$
(fg)(0) \quad (mod \; 2)
$$
That is, we can get the LSB of the product of $fg$ from the function value of 0, and:

+ When the constant term of $g$ is 0, the function value is all 0

+ When the constant term of $g$ is 1, the function value is the LSB of $f$, which is equivalent to obtaining 21333 discontinuous leakage bits of MT19937, so the initial state can be reconstructed for random number prediction, and then get $g$ and all $f$

Therefore, we can repeatedly reconnect to the target machine to check whether the constant term is all 0 under modulo 2. If not, we can solve the matrix equation to get the initial state.

The last problem is the 10s limit. First of all, the matrix can be pre-calculated, but it takes about 20s to solve the matrix equation under normal computing power. The key is that the property of MT19937 determines that its maximum rank is only 19937, so we only need 19937 equations to obtain a full-rank 19937x19937 square matrix. We can pre-calculate the inverse of the square matrix, so that after obtaining the data from remote, we only need to calculate the matrix-vector multiplication once and only cost less than 1s.

> Why not shorten the time limit? Because 10s is just right. If it is shortened further, player may realize that it is not a hidden number problem XD.