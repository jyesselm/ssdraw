import sys
import uuid
sys.path.append("..")

import components, structure_2d
from rnamake import secondary_structure, secondary_structure_parser


def test_residue():
    r = structure_2d.Residue2D("G", "(", 1, "A", uuid.uuid1())
    r.set_pos(0.5, 0.5)

    fig = components.Figure()
    fig.add_component(r.get_obj())

    fig.show()


def test_residues():
    ss = secondary_structure.Structure(sequence="GGAGG",
                                       dot_bracket=".....",
                                       rtype=structure_2d.Residue2D)

    fig = components.Figure()
    x = 0.1
    y = 0.1
    for r in ss.residues():
        r.set_pos(x, y)
        y += 0.025
        fig.add_component(r.get_obj())
    fig.show()


def test_graph_2d():
    ss = secondary_structure.Structure(sequence="GGAAACC",
                                       dot_bracket="((...))",
                                       rtype=structure_2d.Residue2D)

    g = structure_2d.Graph2D(ss)
    print len(g.graph)

test_graph_2d()