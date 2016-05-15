import math

from rnamake import secondary_structure, secondary_structure_parser, motif_type

import components, structure_2d

# use 2D instances instead of default ones
secondary_structure.Factory.residue  = structure_2d.Residue2D
secondary_structure.Factory.basepair = structure_2d.Basepair2D

class Drawer(object):
    def __init__(self):
        self.fig = components.Figure()

        self.NODE_R = 6
        self.PRIMARY_SPACE = 0.025
        self.PAIR_SPACE = 0.04
        self.CELL_PADDING = 40

    def draw(self, seq, ss):
        self.struct = secondary_structure.Structure(sequence=seq,
                                                    dot_bracket=ss)


        p = secondary_structure_parser.SecondaryStructureParser()
        self.motif = p.parse_to_motif(structure=self.struct)
        self.ssg = p.parse_to_motif_graph(structure=self.struct)

        self._setup_coords()

        for r in self.struct.residues():
            self.fig.add_component(r.get_obj())

        self.fig.show()

    def _setup_coords(self):

        first_res = self.struct.residues()[0]
        #first_res.set_pos(0.5, 0.1, 0, 1)

        #bp = self.motif.get_basepair(res1=first_res)
        #if bp is not None:
        #    bp.set_pos(0.5, 0.1, 0, 1)

        for i, n in enumerate(self.ssg.graph):
            if i == 0:
                n.data.basepairs[0].set_pos(0.5, 0.1, 0, 1)

            if n.data.mtype == motif_type.HELIX:
                self._setup_bp_step_coords(n)
            else:
                self._setup_unpaired_coords(n)

    def _setup_bp_step_coords(self, n):
        x, y, go_x, go_y = n.data.basepairs[0].get_pos()

        new_x = x + go_x * self.PRIMARY_SPACE
        new_y = y + go_y * self.PRIMARY_SPACE

        n.data.basepairs[1].set_pos(new_x, new_y, go_x, go_y)

    def _get_unbound_nodes(self, n):
        res = n.data.residues()
        res.remove(n.data.ends[0].res1)
        res.remove(n.data.ends[0].res2)

        bp_res = []
        for bp in n.data.basepairs:
            bp_res.append(bp.res1)
            bp_res.append(bp.res2)

        nodes = []
        seen_bp = []

        for r in res:
            if r not in bp_res:
                nodes.append(r)
            else:
                bp = n.data.get_basepair(res1=r)
                if bp in nodes:
                    continue
                else:
                    nodes.append(bp)


        return nodes

    def _setup_unpaired_coords(self, n):

        nodes = self._get_unbound_nodes(n)

        x, y, go_x, go_y = n.data.basepairs[0].get_pos()

        cross_x = go_y
        cross_y = -go_x


        npairs = len(n.data.ends)-1
        length_walker = self.PAIR_SPACE / 2.0
        circle_length = (len(nodes)+1) * self.PRIMARY_SPACE + (npairs + 1) * self.PAIR_SPACE
        circle_radius = circle_length / (2 * math.pi)

        x = x + go_x * circle_radius
        y = y + go_y * circle_radius

        for i , e in enumerate(nodes):

            length_walker += self.PRIMARY_SPACE

            if isinstance(e, structure_2d.Basepair2D):
                length_walker += self.PAIR_SPACE / 2.0

            rad_angle = -length_walker / circle_length * 2 * math.pi - math.pi / 2.0
            new_x = x + math.cos(rad_angle) * cross_x * circle_radius + \
                  math.sin(rad_angle) * go_x * circle_radius

            new_y = y + math.cos(rad_angle) * cross_y * circle_radius + \
                  math.sin(rad_angle) * go_y * circle_radius

            new_go_x = new_x - x
            new_go_y = new_y - y
            new_go_len = math.sqrt(new_go_x * new_go_x + new_go_y * new_go_y);

            e.set_pos(new_x, new_y, new_go_x / new_go_len, new_go_y / new_go_len)

            if isinstance(e, structure_2d.Basepair2D):
                length_walker += self.PAIR_SPACE / 2.0







