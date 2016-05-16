import sys
import uuid
import random
sys.path.append("..")

import drawer, structure_2d
import constructs

def random_ss(max_size=2):
    s = random.randint(2, max_size)
    seq = "GAAAAC"
    ss =  "(....)"
    seq, ss = add_helix(seq, ss, random.randint(2, 10))
    #for i in range(s):
    for i in range(s):
        seq, ss = add_junction(seq, ss, random.randint(0, 10), random.randint(0, 10))
        seq, ss = add_helix(seq, ss, random.randint(2, 5))

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
    seq, ss = random_ss(5)

    d = drawer.Drawer()
    #d.draw("GGAAGACAAGACAACC",
    #       "((..(.)..(.)..))")
    #d.draw(seq, ss)
    #d.draw("GGGGAAAAAGGAAACAACCAAACCC",
    #       "((((.....((...)..))...)))")
    #d.draw("GGAAG+CCC",
    #       "((..(+)))")

    d.draw(*constructs.group_1_intron)

def test_drawer_2():

    p = structure_2d.get_pose(*constructs.signal_particle)
    #p.update_option('residue_radius', 0.0075)
    d = drawer.Drawer()
    d.draw(pose=p)


test_drawer_2()