import math

from rnamake import secondary_structure, secondary_structure_parser, motif_type

import components, structure_2d

class Drawer(object):
    def __init__(self):
        self.fig = components.Figure()

        self.NODE_R = 6
        self.PRIMARY_SPACE = 0.025
        self.PAIR_SPACE = 0.04
        self.CELL_PADDING = 40



    def draw(self, seq, ss):
        self.struct = secondary_structure.Structure(sequence=seq,
                                                    dot_bracket=ss,
                                                    rtype=structure_2d.Residue2D)


        p = secondary_structure_parser.SecondaryStructureParser()
        self.motif = p.parse_to_motif(structure=self.struct)
        self.ssg = p.parse_to_motif_graph(structure=self.struct)

        self._setup_coords()

        for r in self.struct.residues():
            self.fig.add_component(r.get_obj())

        self.fig.show()

    def _setup_coords(self):

        first_res = self.struct.residues()[0]
        first_res.set_pos(0.5, 0.1, 0, 1)

        bp = self.motif.get_basepair(res1=first_res)
        if bp is not None:
            self._setup_basepair_partner_coords(first_res, bp.partner(first_res))

        for i, n in enumerate(self.ssg.graph):
            if n.data.mtype == motif_type.HELIX:
                self._setup_bp_step_coords(n)
            else:
                self._setup_unpaired_coords(n)

    def _setup_bp_step_coords(self, n):
        x, y, go_x, go_y = n.data.basepairs[0].res1.get_pos()

        # need to propograte coords to second basepair
        r1, r2 = n.data.basepairs[1].res1, n.data.basepairs[1].res2
        new_x = x + go_x * self.PRIMARY_SPACE
        new_y = y + go_y * self.PRIMARY_SPACE

        r1.set_pos(new_x, new_y, go_x, go_y)
        self._setup_basepair_partner_coords(r1, r2)

    def _setup_basepair_partner_coords(self, r, partner):
        cross_x = r.go_y
        cross_y = r.go_x
        new_x = r.x + cross_x * self.PAIR_SPACE
        new_y = r.y - cross_y * self.PAIR_SPACE
        partner.set_pos(new_x, new_y, r.go_x, r.go_y)

    def _get_unbound_nodes(self, n):
        pass

    def _setup_unpaired_coords(self, n):

        x1, y1, go_x, go_y = n.data.basepairs[0].res1.get_pos()
        x2 = n.data.basepairs[0].res2.x
        y2 = n.data.basepairs[0].res2.y

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        cross_x = go_y
        cross_y = -go_x

        res = n.data.residues()
        res.remove(n.data.ends[0].res1)
        res.remove(n.data.ends[0].res2)

        bp_res = []
        for bp in n.data.basepairs:
            bp_res.append(bp.res1)
            bp_res.append(bp.res2)

        npairs = len(n.data.ends)-1
        length_walker = self.PAIR_SPACE / 2.0
        circle_length = (len(res)+1) * self.PRIMARY_SPACE + (npairs + 1) * self.PAIR_SPACE
        circle_radius = circle_length / (2 * math.pi)

        x = x + go_x * circle_radius
        y = y + go_y * circle_radius

        for i ,r in enumerate(res):

            length_walker += self.PRIMARY_SPACE

            rad_angle = -length_walker / circle_length * 2 * math.pi - math.pi / 2.0
            r.x = x + math.cos(rad_angle) * cross_x * circle_radius + \
                  math.sin(rad_angle) * go_x * circle_radius

            r.y = y + math.cos(rad_angle) * cross_y * circle_radius + \
                  math.sin(rad_angle) * go_y * circle_radius

            child_go_x = r.x - x
            child_go_y = r.y - y
            child_go_len = math.sqrt(child_go_x * child_go_x + child_go_y * child_go_y);

            r.go_x = child_go_x / child_go_len
            r.go_y = child_go_y / child_go_len


            if r in bp_res:
                length_walker += self.PAIR_SPACE / 2.5

        for bp in n.data.basepairs:
            x1, y1, go_x1, go_y1 = bp.res1.get_pos()
            x2, y2, go_x2, go_y2 = bp.res2.get_pos()

            new_x = (x1 + x2) / 2
            new_y = (y1 + y2) / 2

            child_go_x = new_x - x
            child_go_y = new_y - y
            child_go_len = math.sqrt(child_go_x * child_go_x + child_go_y * child_go_y);

            bp.res1.go_x = child_go_x / child_go_len
            bp.res1.go_y = child_go_y / child_go_len





