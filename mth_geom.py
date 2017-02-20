#!/usr/bin/env python
#coding=utf8
"""
New program
"""
import argparse

from cjh.maths.angles import Angle
from cjh.maths.geometry import Graph, Point
from cjh.misc import notebook

import easycat
from versatiledialogs.terminal import Terminal, ListPrompt

__author__ = 'Chris Horn <hammerhorn@gmail.com>'
__license__ = 'GPL'


REMARKS = """
    - use letterator to name pts
    - label the scale
    - givr more distances
    - see if scalar is working
    - domain max and min for polynom or function
    - learn to shade areas of the graph
"""


Terminal()

################
#  PROCEDURES  #
################
def _parse_args():
    """
    Parse arguments
    """
    notebook(REMARKS)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-C', action='store_true', help="read developer's comments")
    return parser.parse_args() if __name__ == '__main__' else None


def two_points():
    """
    gets two points from stdin, prints the distance to stdout

    use makepage?
    """
    points = []
    graph = Graph()
    for count in range(2):
        points.append(Point(0, 0))
        points[count].input(
            prompt=Terminal.fx('un', 'Point {}'.format(count + 1)))

        graph.plot_point(points[count].x, points[count].y)#tuple() func?
        Terminal.clear()
        easycat.write(points[count].__repr__())
        Terminal.output(points[count])
        Terminal.output(graph)
        if count == 1:
            Terminal.output('\n\t{} = {}\n'.format(Terminal.fx(
                'bn', 'distance'), points[1] - points[0]))
        Terminal.wait()


    points.append(Point(0, 0))
    points[2].input(prompt=Terminal.fx('un', 'Point 3'))
    easycat.write(points[2].__repr__())
    Terminal.output(points[2])
    graph.plot_point(points[2].x, points[2].y)  # tuple() func?
    Terminal.clear()
    easycat.write(points[2].__repr__())
    Terminal.output(points[2])
    Terminal.output(graph)
    area = abs((
        points[0].x * (
            points[1].y - points[2].y) + points[1].x * (
                points[2].y - points[0].y) + points[2].x * (
                    points[0].y - points[1].y))/2.0)
    Terminal.output('\n\t{} = {} units²\n'.format(Terminal.fx('bn', 'area'), area))
    Terminal.wait()

def angle_to_slope():
    """
    gets degrees from stdin, prints slope to stdout
    """
    degrees = float(Terminal.input('angle in degrees: '))
    theta = Angle(degrees, 'deg')
    Terminal.output(''.join(('\n\t', theta.pi_radians().__str__(),
                             '\n\tslope = {}\n'.format(theta.slope()))))
    Terminal.wait()
    Terminal.clear(16)

##########
#  DATA  #
##########
ARGS = _parse_args()

##########
#  MAIN  #
##########
def main():
    """
    Main function
    """
    option_tuple = ('two points', 'angle to slope', 'plot an ellipse')

    # Maybe an OrderedDict would work here
    # option_dict = {'two points': two_points, 'angle to slope': angle_to_slope,
    #     'plot an ellipse': lambda: 0}
    menu = ListPrompt(option_tuple)

    while True:
        Terminal.output('')
        option = menu.input() - 1
        Terminal.output('')
        #option_dict
        
        if option_tuple[option] == 'two points':
            two_points()

        elif option_tuple[option] == 'angle to slope':
            angle_to_slope()

        elif option_tuple[option] == 'plot an ellipse':
            pass


if __name__ == '__main__':
    main()
    Terminal.start_app()
