import libsemigroups_cppyy

from libsemigroups_cppyy.todd_coxeter import *

def symgroup(n):
    s = ["s%i"%i for i in range(n)]
    res = []
    for i in range(1,n):
        res.append([[s[i],s[i]], [1]])
    for i in range(1, n-1):
        res.append([[s[i],s[i+1],s[i]], [s[i+1],s[i],s[i+1]]])
    for i in range(1, n-2):
        for j in range(i+2, n):
            res.append([[s[i],s[j]], [s[j],s[i]]])
    return s[1:], res
def Hecke0(n):
    p = ["pi%i"%i for i in range(n)]
    res = []
    for i in range(1,n):
        res.append([[p[i],p[i]], [1]])
    for i in range(1, n-1):
        res.append([[p[i],p[i+1],p[i]], [p[i+1],p[i],p[i+1]]])
    for i in range(1, n-2):
        for j in range(i+2, n):
            res.append([[p[i],p[j]], [p[j],p[i]]])
    return p[1:], res


N = 5

gs, rs = symgroup(N)
SG = make_cong([1]+gs, rs, identity=1)
SG.run()
SG.standardize(ToddCoxeter.order.shortlex)
clSG = classes_reduced_word_cong(SG)

gs, rs = Hecke0(N)
H0 = make_cong([1]+gs, rs, identity=1)
H0.run()
H0.standardize(ToddCoxeter.order.shortlex)
clH0 = classes_reduced_word_cong(H0)

print (clSG == clH0)





