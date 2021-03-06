#!/usr/bin/env python

import math
import argparse

import secondary_structure, secondary_structure_parser, motif_type
import secondary_structure_graph

import components, structure_2d


class Drawer(object):
    """
    Draws a secondary structure either from a sequence and dot bracket secondary
    structure or from a secondary_structure.Pose object

    :param seq: sequence of structure you want to draw
    :param ss:  dot bracket notation of structure you want to draw
    :param pose: secondary_structure.Pose that you have created in advance
        that you want to draw

    :type seq: Str
    :type ss: Str
    :type pose: secondary_structure.Pose

    """

    def __init__(self):
        self.fig = components.Figure()

        self.residue_spacing = 0.025
        self.pair_space = 0.04
        self.draw_names = 1

        self.pose = None
        self.ssg  = None

    def draw(self, seq=None, ss=None, pose=None):

        self._setup(seq, ss, pose)

        for r in self.pose.residues():
            self.fig.add_component(r.get_obj())
            if self.draw_names:
                self.fig.add_text(r.x, r.y+r.radius/7, r.name,
                                   fontsize=self.pose.get_option('name_size'))

        self.fig.show()

    def save_fig(self, fname="test.pdf"):
        self._setup(seq, ss, pose)

        for r in self.pose.residues():
            self.fig.add_component(r.get_obj())
            if self.draw_names:
                # writing to pdf has everything shifted slightly, and some
                # letters more then others for some reason A is not nearly as
                # effected
                if r.name != "A":
                    self.fig.add_text(r.x-r.radius/7, r.y-r.radius/7, r.name,
                                  fontsize=self.pose.get_option('name_size'))
                else:
                    self.fig.add_text(r.x, r.y-r.radius/7, r.name,
                                  fontsize=self.pose.get_option('name_size'))

        self.fig.save(fname)

    def _setup(self, seq, ss, pose):
        if pose is None:
            p = secondary_structure_parser.SecondaryStructureParser()
            self.pose = p.parse_to_pose(sequence=seq, dot_bracket=ss)
        else:
            self.pose = pose

            # copy options from pose
            self.residue_spacing = self.pose.get_option('residue_spacing')
            self.pair_space      = self.pose.get_option('pair_space')
            self.draw_names      = self.pose.get_option('draw_names')

        self.ssg = secondary_structure_graph.graph_from_pose(self.pose)
        self._setup_coords()

    def _setup_coords(self):

        first_res = self.pose.residues()[0]
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

        new_x = x + go_x * self.residue_spacing
        new_y = y + go_y * self.residue_spacing

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
        """
        draws unpaired residues in a circle

        :param n:
        :return:
        """

        nodes = self._get_unbound_nodes(n)

        x, y, go_x, go_y = n.data.basepairs[0].get_pos()

        cross_x = go_y
        cross_y = -go_x

        npairs = len(n.data.ends)-1
        length_walker = self.pair_space / 2.0
        circle_length = (len(nodes)+1) * self.residue_spacing + (npairs + 1) * self.pair_space
        circle_radius = circle_length / (2 * math.pi)

        x = x + go_x * circle_radius
        y = y + go_y * circle_radius

        for i , e in enumerate(nodes):

            length_walker += self.residue_spacing

            if isinstance(e, structure_2d.Basepair2D):
                length_walker += self.pair_space / 2.0

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
                length_walker += self.pair_space / 2.0

def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-ss', help='path', required=True)
    parser.add_argument('-seq', required=True)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    d = Drawer()
    d.draw(seq=args.seq, ss=args.ss)



if __name__ == '__main__':
    main()







