import sys
import uuid
import random
sys.path.append("..")

import drawer

def random_ss(max_size=2):
    s = random.randint(2, max_size)
    seq = "GAAAAC"
    ss =  "(....)"
    seq, ss = add_helix(seq, ss, random.randint(2, 10))
    #for i in range(s):
    seq, ss = add_junction(seq, ss, random.randint(0, 10), random.randint(0, 10))

    seq, ss = add_helix(seq, ss, random.randint(2, 10))

    return seq, ss

def add_helix(seq, ss, size):
    for i in range(size):
        seq = "G" + seq + "C"
        ss =  "(" + ss  + ")"

    return seq, ss

def add_junction(seq, ss, x_size, y_size):
    for i in range(x_size):
        seq = "A" + seq
        ss  = "." + ss

    for i in range(y_size):
        seq = seq + "A"
        ss = ss + "."

    return seq, ss

def test_drawer():
    #seq, ss = random_ss()

    d = drawer.Drawer()
    d.draw("GGAAGACAAGACAACC",
           "((..(.)..(.)..))")
    #d.draw(seq, ss)
    #d.draw("GGGGAAAAAGGAAACAACCAAACCC",
    #       "((((.....((...)..))...)))")
    #d.draw("GGAAAGCAAGCAGCAACC", "((...()..().()..))")


test_drawer()