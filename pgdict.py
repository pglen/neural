#!/usr/bin/env python

import sys, random

class DeepDict(dict):

    ''' Automatically create new dimentions '''

    def setdeep(self, dims, val):
        #print("setdeep", dims)
        hist = self
        for cnt, aa in enumerate(dims):
            if cnt == len(dims)-1:
                if aa in hist:
                    if isinstance(hist[aa], dict):
                        #print("Warn: key exists", aa)
                        raise ValueError("Dimension exists already", aa)

                hist.setdefault(aa, val)
            else:
                if not aa in hist:
                    # Create if not present
                    hist.setdefault(aa, {})
            hist = hist[aa]

    def getdim(self, dim):

        ''' Get value for dimention '''

        hist = self
        for aa in dim:
            # Generate exception if not in dict
            if isinstance(hist[aa], dict):
                pass
            hist = hist[aa]

        #for bb in hist:
        #    print(bb)
        return hist

    def recurse(self, idx = [], callb = None):
        #print("recurse ttt:", self)
        #print("recurse idx =", idx)
        nnn = self
        # Build index
        for aaa in idx:
            if isinstance(nnn[aaa], dict):
                nnn = nnn[aaa]
        #print("nnn =", nnn)
        for aaaa in nnn:
            #print("re", aaaa)
            if isinstance(nnn[aaaa], dict):
                idx.append(aaaa)
                self.recurse(idx, callb)
            else:
                idx2 = idx + [aaaa,]
                #print("idx =", idx2, "val =", nnn[aaaa])
                if callb:
                    callb(idx2, nnn[aaaa])

    def __getitem__(self, key):
        #print("getitem key =", key)
        if isinstance(key, tuple):
            ret = self.getdim(key)
        else:
            if key not in self:
                super().setdefault(key, {})
            ret = super().__getitem__(key)
        return ret

    def __setitem__(self, key, value):
        #print("setitem", key, type(key), value, type(value))
        if isinstance(key, tuple):
            #print("tuple", key)
            self.setdeep(key, value)
        else:
            try:
                super().__getitem__(key)
            except:
                pgutil.print_exception("set -> get")
                #print("set", sys.exc_info())
                #super().__setitem__(key, value)
                super().__setitem__(key, {})

    #def __delitem__(self, key, value):
    #    if isinstance(key, tuple):
    #        for k in key: super().__delitem__(k)
    #    else:
    #        super().__setitem__(key, value)

def callit(idx, val):
    print("callb:", idx, val)

if __name__ == '__main__':

    import  pgutil

    ddd = DeepDict()
    ddd[1,2,3] = 88
    ddd[1,2,4] = 99
    print("ddd =", ddd)
    print("ddd[1,2] =", ddd[1,2])
    print("ddd[1,2,3] =", ddd[1,2,4])

    ttt = DeepDict()
    ttt.setdeep((1, 2, 3, 4), 'a')
    ttt.setdeep((1, 2, 3, 5), 'b')
    # This sould raise exception
    #ttt.setdeep((1, 2, 3), 'c')
    ttt.setdeep((1, 2, 6), 'd')
    print("ttt =", ttt)
    ttt.recurse(callb=callit)

    print("getdim[1.2]:", ttt.getdim((1,2 )))
    print("getdim[1,2,3]:", ttt.getdim((1,2,3 )))
    print("getdim[1,2,3,4]:", ttt.getdim((1,2,3,4 )))

    assert 1 == 1

    nn = DeepDict()
    nn.setdeep((0,), 'b')
    print("nn =", nn)

# EOF
