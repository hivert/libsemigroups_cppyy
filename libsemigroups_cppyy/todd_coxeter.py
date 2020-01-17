"""
This file contains the interface to the implementation of the
Todd-Coxeter algorithm for finitely presented semigroups in libsemigroups; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__congruence__toddcoxeter.html

for further details.


"""
import cppyy
cppyy.include("cong.hpp")
cppyy.include("cong-intf.hpp")

lsg = cppyy.gbl.libsemigroups
congruence_type = lsg.congruence_type
ToddCoxeter = lsg.congruence.ToddCoxeter

def make_cong(lgen, rels, identity=None):
    """
    Build a congruence

    each generator must be hashable.

    - `lgen` : the list of generators (must be unique)
    - `rels` : a list of pairs of tuple
    - `identity` : the identity if known

    if `rels` contains a generator which is not in `lgen`, it will be appended.
    """
    if len(set(lgen)) != len(lgen):
        raise ValueError("duplicate generator")
    if identity is not None and identity not in lgen:
        lgen.append(identity)
    for rel in rels:
        for w in rel:
            for g in w:
                if g not in lgen:
                    lgen.append(g)
    res = ToddCoxeter(lsg.congruence_type.twosided)
    res.set_nr_generators(len(lgen))
    def add_pair(a,b) :
        # print("Adding : (%s, %s)"%(a,b))
        res.add_pair(a,b)
    if identity is not None:
        idd = lgen.index(identity)
        for ig in range(len(lgen)):
            add_pair([ig, idd], [ig])
            if idd != ig:
                add_pair([idd, ig], [ig])
    def iword(w):
        return [lgen.index(l) for l in w]
    for rel in rels:
        trg = iword(rel[0])
        for src in rel[1:]:
            add_pair(trg, iword(src))
    return res


def classes_reduced_word_cong(C):
    r"""
    returns the list of the classes all the reduced words.

    Each classes is stored as a frozenset. in the same order as the
    index of `C`.
    """
    res = []
    for nc in range(C.nr_classes()):
        w =  C.class_index_to_word(nc)
        Cl = []
        for wrd in lsg.shortlex_words(C.nr_generators(), w.size(), w.size()):
            if (C.word_to_class_index(wrd) == nc):
                Cl.append(tuple(wrd))
        res.append(frozenset(Cl))
    return res
