#!/usr/bin/env python

import sys, random

class EasyDict(dict):
    def __getitem__(self, key):
        if isinstance(key, tuple):
            return [super().__getitem__(k) for k in key]
        else:
            return super().__getitem__(key)
    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            self.update(zip(key, value))
        else:
            super().__setitem__(key, value)
    def __delitem__(self, key, value):
        if isinstance(key, tuple):
            for k in key: super().__delitem__(k)
        else:
            super().__setitem__(key, value)

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
        hist = self
        try:
            for aa in dim:
                hist = hist[aa]
            #print("dim", hist)
            #for bb in hist:
            #    print(bb)
        except:
            pass
            print("getdim:", sys.exc_info())
            raise

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

        #def __getitem__(self, key):
        #    #print("getitem key =", key)
        #    if key not in self:
        #        super().setdefault(key, {})
        #    ret = super().__getitem__(key)
        #    return ret
        #def __setitem__(self, key, value):
        #    #print("setitem", key, value, type(value))
        #    try:
        #        super().__getitem__(key)
        #    except:
        #        pgutil.print_exception("set -> get")
        #        #print("set", sys.exc_info())
        #        #super().__setitem__(key, value)
        #        super().__setitem__(key, {})
        #def __delitem__(self, key, value):
        #    if isinstance(key, tuple):
        #        for k in key: super().__delitem__(k)
        #    else:
        #        super().__setitem__(key, value)

def callit(idx, val):
    print("callb:", idx, val)

if __name__ == '__main__':

    import  pgutil
    ttt = DeepDict()
    ttt.setdeep((1, 2, 3, 4), 'a')
    ttt.setdeep((1, 2, 3, 5), 'b')
    #ttt.setdeep((1, 2, 3), 'c')
    ttt.setdeep((1, 2, 6), 'd')
    print("ttt =", ttt)
    ttt.recurse(callb=callit)

    print("getdim:", ttt.getdim((1,2 )))
    #nn = DeepDict()
    #nn.setdeep((1,), 'b')
    #print(nn)

# EOF
