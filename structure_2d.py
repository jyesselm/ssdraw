from rnamake import secondary_structure, secondary_structure_parser, graph
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

    def set_pos(self, x, y, go_x=None, go_y=None):
        self.x = x
        self.y = y
        if go_x is not None:
            self.go_x = go_x
        if go_y is not None:
            self.go_y = go_y

        cross_x = go_y
        cross_y = -go_x

        self.res1.set_pos( x + cross_x * settings.PAIR_SPACE / 2.0,
                           y + cross_y * settings.PAIR_SPACE / 2.0,
                           go_x, go_y)

        self.res2.set_pos( x - cross_x * settings.PAIR_SPACE / 2.0,
                           y - cross_y * settings.PAIR_SPACE / 2.0,
                           go_x, go_y)



    def get_pos(self):
        return self.x, self.y, self.go_x, self.go_y





