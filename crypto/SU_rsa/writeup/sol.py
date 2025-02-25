import itertools
from sage.rings.polynomial.multi_polynomial_sequence import PolynomialSequence
def flatter(M):
    from subprocess import check_output
    from re import findall
    z = "[[" + "]\n[".join(" ".join(map(str, row)) for row in M) + "]]"
    ret = check_output(["flatter"], input=z.encode())
    return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\\d+", ret)))

def small_roots(f, X, beta=1.0, m=None):
    N = f.parent().characteristic()
    delta = f.degree()
    if m is None:
        epsilon = RR(beta^2/f.degree() - log(2*X, N))
        m = max(beta**2/(delta * epsilon), 7*beta/delta).ceil()
    t = int((delta*m*(1/beta - 1)).floor())
    f = f.monic().change_ring(ZZ)
    P,(x,) = f.parent().objgens()
    g = [x**j * N**(m-i) * f**i for i in range(m) for j in range(delta)]

    g.extend([x**i * f**m for i in range(t)])
    B = Matrix(ZZ, len(g), delta*m + max(delta,t))
    for i in range(B.nrows()):
        for j in range(g[i].degree()+1):
            B[i,j] = g[i][j]*X**j
    B = flatter(B)
    f = sum([ZZ(B[0,i]//X**i)*x**i for i in range(B.ncols())])
    roots = set([f.base_ring()(r) for r,m in f.roots() if abs(r) <=
    X])
    return [root for root in roots if N.gcd(ZZ(f(root))) >= N**beta]
d_m =  54846367460362174332079522877510670032871200032162046677317492493462931044216323394426650814743565762481796045534803612751698364585822047676578654787832771646295054609274740117061370718708622855577527177104905114099420613343527343145928755498638387667064228376160623881856439218281811203793522182599504560128
n =  102371500687797342407596664857291734254917985018214775746292433509077140372871717687125679767929573899320192533126974567980143105445007878861163511159294802350697707435107548927953839625147773016776671583898492755338444338394630801056367836711191009369960379855825277626760709076218114602209903833128735441623
e =  112238903025225752449505695131644979150784442753977451850362059850426421356123
k = (e*d_m-1)//n + 1
s = (n+1+inverse_mod(k, e))%e
PR.<x> = PolynomialRing(Zmod(e))
f = x^2-s*x+n
p0 = int(f.roots()[0][0])
PR.<x0> = PolynomialRing(Zmod(n))
for i in range(0, 2**6):
    f = e*(x0+2**250*i)+p0
    root = small_roots(f, X=2**250, beta=0.48, m=25)
    print(root)
x0 = 769306974883685623850311905036778346829296744303179040979107875413
852719182
p = e*(x0+2**250*44)+p0
q = n//p