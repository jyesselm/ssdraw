from rnamake import secondary_structure, secondary_structure_parser, graph, base
from rnamake import option
import components, settings

class Residue2D(secondary_structure.Residue):
    def __init__(self,  name, dot_bracket, num, chain_id, uuid, i_code=""):
        super(self.__class__, self).__init__( name, dot_bracket, num, chain_id, uuid, i_code)

        if self.name == "A":
            self.facecolor = 'orange'
        elif self.name == "G":
            self.facecolor = 'red'
        elif self.name == "U":
            self.facecolor = 'blue'
        elif self.name == "C":
            self.facecolor = 'green'
        else:
            self.facecolor = 'black'

        # coords
        self.x = 0
        self.y = 0
        self.go_x = 0
        self.go_y = 0

        # drawing info
        self.radius = 0.01
        self.edgecolor = 'black'
        self.edgewidth = 1.0
        self.edgestyle = 'solid'

    def set_pos(self, x, y, go_x=None, go_y=None):
        self.x = x
        self.y = y
        if go_x is not None:
            self.go_x = go_x
        if go_y is not None:
            self.go_y = go_y

    def get_pos(self):
        return self.x, self.y, self.go_x, self.go_y

    def get_obj(self):
        return components.get_circle(self.x, self.y, radius=self.radius,
                                     facecolor=self.facecolor,
                                     edgecolor=self.edgecolor,
                                     edgewidth=self.edgewidth,
                                     edgestyle=self.edgestyle)


class Basepair2D(secondary_structure.Basepair):
    def __init__(self, res1, res2, bp_uuid=None):
        super(self.__class__, self).__init__(res1, res2, bp_uuid)

        self.x = 0
        self.y = 0
        self.go_x = 0
        self.go_y = 0
        self.pair_space = settings.PAIR_SPACE

    def set_pos(self, x, y, go_x=None, go_y=None):
        self.x = x
        self.y = y
        if go_x is not None:
            self.go_x = go_x
        if go_y is not None:
            self.go_y = go_y

        cross_x = go_y
        cross_y = -go_x

        self.res1.set_pos( x + cross_x * self.pair_space / 2.0,
                           y + cross_y * self.pair_space / 2.0,
                           go_x, go_y)

        self.res2.set_pos( x - cross_x * self.pair_space / 2.0,
                           y - cross_y * self.pair_space / 2.0,
                           go_x, go_y)



    def get_pos(self):
        return self.x, self.y, self.go_x, self.go_y


class Pose2D(secondary_structure.Pose):
    def __init__(self,  structure=None, basepairs=None, ends=None,
                 name="assembled", path="assembled", score=0, end_ids=None,
                 r_struct=None):

        super(self.__class__, self).__init__(
            structure, basepairs, ends, name, path, score, end_ids, r_struct)

        self.setup_options_and_constraints()

    def setup_options_and_constraints(self):

        options = {'residue_radius' : 0.01,
                   'residue_spacing': 0.025,
                   'pair_space'     : 0.04,
                   'scale'          : 1,
                   'draw_names'     : 1}

        self.defaults = { name : value for name, value in  options.items() }
        self.options = option.Options(options)

    def update_option(self, name, value):
        opt = self.options.get(name)

        needs_scale = 0
        if name == 'residue_radius':
            ratio = value / self.options.get('residue_radius')
            rs = self.options.get('residue_spacing')
            ps = self.options.get('pair_space')

            self.options.set('residue_spacing',  ratio*rs)
            self.options.set('pair_space', ratio*ps)

            for r in self.residues():
                r.radius = value

            for bp in self.basepairs:
                bp.pair_space = ratio*ps

    def get_option(self, name):
        return self.options.get(name)










def get_pose(seq, ss):
    p = secondary_structure_parser.SecondaryStructureParser()
    return p.parse_to_pose(sequence=seq, dot_bracket=ss)

# use 2D instances instead of default ones
secondary_structure.Factory.residue  = Residue2D
secondary_structure.Factory.basepair = Basepair2D
secondary_structure.Factory.pose     = Pose2D
