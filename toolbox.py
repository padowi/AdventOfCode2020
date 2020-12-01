#!/usr/bin/env python3

import re
import math

from collections import defaultdict, Counter, deque

def ints(s):
# {{{
    """
    >>> ints('1,2,3,-1,150')
    [1, 2, 3, -1, 150]
    >>> ints('1 2 3 -1 150')
    [1, 2, 3, -1, 150]
    >>> ints('1\\n2\\n')
    [1, 2]
    """
    p = r'(-?[0-9]+)'
    return list(map(int, re.findall(p, s)))
# }}}


def minmax(a, b):
# {{{
    """
    >>> minmax(1, 2)
    (1, 2)
    >>> minmax(2, 1)
    (1, 2)
    >>> minmax(-1, -5)
    (-5, -1)
    """
    return (min(a, b), max(a, b))
# }}}

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def manhattan(p1, p2):
# {{{
    """
    >>> manhattan( (0, 0), (1, 1) )
    2
    """
    x1,y1 = p1
    x2,y2 = p2
    minX, maxX = minmax(x1, x2)
    minY, maxY = minmax(y1, y2)
    return (maxX - minX) + (maxY - minY)
# }}}

def point_on_line(point, line):
# {{{
    """
    >>> point_on_line((1, 1), ((0, 0), (2, 2)))
    True
    >>> point_on_line((5, 5), ((0, 0), (2, 2)))
    False
    """
    cpX, cpY = point
    (p1X, p1Y), (p2X, p2Y) = line

    delta_cpXp1X = cpX - p1X
    delta_cpYp1Y = cpY - p1Y

    delta_lineX = p2X - p1X
    delta_lineY = p2Y - p1Y

    cross = delta_cpXp1X * delta_lineY - delta_cpYp1Y * delta_lineX

    if cross != 0:
        return False

    if (abs(delta_lineX) >= abs(delta_lineY)):
        if delta_lineX > 0:
            return p1X <= cpX and cpX <= p2X
        else:
            return p2X <= cpX and cpX <= p1X
    else:
        if delta_lineY > 0:
            return p1Y <= cpY and cpY <= p2Y
        else:
            return p2Y <= cpY and cpY <= p1Y
# }}}


class Intcode(object):
    def __init__(self, program, inputStream=deque(), outputStream=deque(), debug=False):
        self._program = defaultdict(lambda: 0)
        for idx, val in enumerate(program):
            self._program[idx] = val
        self._input = inputStream
        self._output = outputStream
        self._cursor = 0 # the "instruction pointer"
        self._relative_base = 0
        self._opcodes = {
            1: self._op_add,
            2: self._op_multiply,
            3: self._op_input_at,
            4: self._op_output_from,
            5: self._op_jump_if_true,
            6: self._op_jump_if_false,
            7: self._op_less_than,
            8: self._op_equals,
            9: self._op_adjust_relative_base,
            99: self._op_halt,
        }
        self._last_opcode_executed = None
        self._debug = debug

    def set_input_stream(self, inputStream):
        self._input = inputStream


    def set_output_stream(self, outputStream):
        self._output = outputStream


    def push_input(self, val):
        self._input.append(int(val))


    def has_output(self):
        return len(self._output) > 0


    def pop_output(self):
        return self._output.popleft()


    def peek_latest_output(self):
        return self._output[-1]


    def modify_program(self, pos, val):
        self._program[pos] = val


    def dump_program_state(self):
        return self._program


    def _parse_modes(self, arity):
        opcode = self._program[self._cursor]
        if opcode < 100:
            # legacy mode, set modes for all parameters to 0
            modes = [0] * arity
        else:
            modes = [int(i) for i in str(opcode)[0:-2]]
            while len(modes) < arity:
                modes.insert(0, 0)

        modes.reverse()
        return modes


    def _op_add(self):
        arity = 3
        modes = self._parse_modes(arity)

        cursor_offset = 1
        p1ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)
        cursor_offset = 2
        p2ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)
        cursor_offset = 3
        p3ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)

        self._program[p3ptr] = self._program[p1ptr] + self._program[p2ptr]
        self._cursor += arity + 1


    def _op_multiply(self):
        arity = 3
        modes = self._parse_modes(arity)

        cursor_offset = 1
        p1ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)
        cursor_offset = 2
        p2ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)
        cursor_offset = 3
        p3ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)

        self._program[p3ptr] = self._program[p1ptr] * self._program[p2ptr]
        self._cursor += arity + 1


    def _op_input_at(self):
        arity = 1
        if len(self._input) > 0:
            modes = self._parse_modes(arity)
            cursor_offset = 1
            ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)
            self._program[ptr] = self._input.popleft()
            self._cursor += arity + 1
        else:
            self._op_halt()


    def _op_output_from(self):
        arity = 1
        modes = self._parse_modes(arity)

        cursor_offset = 1
        ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)

        self._output.append(self._program[ptr])
        self._debug and print(self._program[ptr]) # XXX: for visual diagnostics, don't remove!
        self._cursor += arity + 1


    def _op_jump_if_true(self):
        arity = 2
        modes = self._parse_modes(arity)

        cursor_offset = 1
        ptr1 = self._get_pointer(modes[cursor_offset-1], cursor_offset)
        if self._program[ptr1] != 0:
            cursor_offset = 2
            ptr2 = self._get_pointer(modes[cursor_offset-1], cursor_offset)
            self._cursor = self._program[ptr2]
        else:
            self._cursor += arity + 1


    def _op_jump_if_false(self):
        arity = 2
        modes = self._parse_modes(arity)

        cursor_offset = 1
        ptr1 = self._get_pointer(modes[cursor_offset-1], cursor_offset)
        if self._program[ptr1] == 0:
            cursor_offset = 2
            ptr2 = self._get_pointer(modes[cursor_offset-1], cursor_offset)
            self._cursor = self._program[ptr2]
        else:
            self._cursor += arity + 1


    def _op_less_than(self):
        arity = 3
        modes = self._parse_modes(arity)

        cursor_offset = 1
        p1ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)
        cursor_offset = 2
        p2ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)
        cursor_offset = 3
        p3ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)

        self._program[p3ptr] = 1 if self._program[p1ptr] < self._program[p2ptr] else 0
        self._cursor += arity + 1


    def _op_equals(self):
        arity = 3
        modes = self._parse_modes(arity)

        cursor_offset = 1
        p1ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)
        cursor_offset = 2
        p2ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)
        cursor_offset = 3
        p3ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)

        self._program[p3ptr] = 1 if self._program[p1ptr] == self._program[p2ptr] else 0
        self._cursor += arity + 1


    def _op_adjust_relative_base(self):
        arity = 1
        modes = self._parse_modes(arity)

        cursor_offset = 1
        ptr = self._get_pointer(modes[cursor_offset-1], cursor_offset)

        self._relative_base = self._relative_base + self._program[ptr]
        self._cursor += arity + 1


    def _op_halt(self):
        raise StopIteration


    def _get_pointer(self, mode, offset):
        if mode == 0:
            ptr = self._program[self._cursor + offset]
        elif mode == 1:
            ptr = self._cursor + offset
        elif mode == 2:
            # TODO: did I get this right?
            ptr = self._relative_base + self._program[self._cursor + offset]
        else:
            print("ERROR: This should never happen")
            sys.exit(1)

        return ptr


    def get_last_executed_opcode(self):
        return self._last_opcode_executed


    def execute_instruction(self):
        opcode = int(str(self._program[self._cursor])[-2:])
        self._last_opcode_executed = opcode
        self._opcodes[opcode]()


    def run(self):
        while True:
            try:
                self.execute_instruction()
            except StopIteration:
                break


class SpaceImageFormat(object):
    def __init__(self, width, height, sequence):
        self._width = width
        self._height = height
        self._sequence = sequence
        self._num_layers = int(len(sequence) / (width * height))
        self._stats = dict()
        self._render_image()
        self._decode = defaultdict(list)
        self._colors = {
            0: 'black',
            1: 'white',
            2: 'transparent',
        }

    def _render_image(self):
        self._image = dict()
        for layerId in range(self._num_layers):
            self._image[layerId] = dict()
            self._stats[layerId] = Counter()
            for rowId in range(self._height):
                self._image[layerId][rowId] = list()
                for colId in range(self._width):
                    value = self._sequence.pop(0)
                    self._image[layerId][rowId].append(value)
                    self._stats[layerId][value] += 1


    def antiCorruption(self):
        layerWithFewestZeroes = None
        for layerId in self._stats.keys():
            if not layerWithFewestZeroes:
                layerWithFewestZeroes = layerId
                continue
            contestant = self._stats[layerId]
            champion = self._stats[layerWithFewestZeroes]

            if contestant[0] < champion[0]:
                layerWithFewestZeroes = layerId
        return self._stats[layerWithFewestZeroes][1] * self._stats[layerWithFewestZeroes][2]

    def decode(self):
        # plan of attack:
        # for each coordinate (width, height) # generate a list containing the
        # value of each such pixel, across its layers
        # store these lists in a dict, with coord as key
        # for each list, while list[0] == 0, pop that item
        # then, once we have stopped the popping, the value is either 1 or 2
        for x in range(self._width):
            for y in range(self._height):
                coord = (x, y)
                for layerId in range(self._num_layers):
                    self._decode[coord].append(self._image[layerId][y][x])

        for coord in self._decode.keys():
            pixels = self._decode[coord]
            while pixels[0] == 2:
                pixels.pop(0)
            self._decode[coord] = pixels[0]

        for y in range(self._height):
            print("")
            for x in range(self._width):
                coord = (x, y)
                print(' ' if self._decode[coord] == 0 else 'X', end="")


def getQuadOf(origin, other):
# {{{
    """
    >>> getQuadOf((2, 2), (1, 0))
    'NW'
    >>> getQuadOf((2, 2), (2, 0))
    'N'
    >>> getQuadOf((2, 2), (4, 1))
    'NE'
    >>> getQuadOf((2, 2), (0, 2))
    'W'
    >>> getQuadOf((2, 2), (4, 2))
    'E'
    >>> getQuadOf((2, 2), (0, 3))
    'SW'
    >>> getQuadOf((2, 2), (2, 4))
    'S'
    >>> getQuadOf((2, 2), (3, 4))
    'SE'
    >>> getQuadOf((2, 2), (2, 2))
    
    """
    if origin == other:
        return None

    ax, ay = origin
    bx, by = other

    if ax == bx:
        # on same longitude, only N/S matters
        if ay > by: # other is to the West of origin
            return 'N'
        else: # we have already checked that they are not identical
            # and we know that X is same, so Y cannot be same, so if
            # ay isn't greater than by, then it must be smaller,
            # in which case by is greater than (to the right / East of) origin
            return 'S'

    if ay == by:
        if ax > bx: # origin is below other
            return 'W'
        else:
            return 'E'

    direction = list()
    if ay < by:
        direction.append('S')
    else:
        direction.append('N')
    if ax < bx:
        direction.append('E')
    else:
        direction.append('W')

    return ''.join(direction)
# }}}


def gcd(a, b):
    if a == 0: return abs(b)
    if b == 0: return abs(a)
    if a == b: return abs(a)
    if a > b: return gcd(a - b, b)
    else: return gcd(a, b - a)


def determineSmallestGradientBetween(asteroid, otherAsteroid):
# {{{
    """
    >>> determineSmallestGradientBetween((2, 2), (5, 4))
    (3, 2)
    >>> determineSmallestGradientBetween((2, 2), (8, 6))
    (3, 2)
    >>> determineSmallestGradientBetween((1, 0), (4, 0))
    (1, 0)
    """
    if asteroid == otherAsteroid:
        return None

    x1, y1 = asteroid
    x2, y2 = otherAsteroid
    dx = otherAsteroid[0] - asteroid[0]
    dy = otherAsteroid[1] - asteroid[1]

    # we need to handle the case where the delta of either x or y == 0
    # since division by 0 is bad mmmm'kay
    if dx == 0:
        # either dy is > 0 or < 0
        if dy > 0: return (0, 1)
        else: return (0, -1)
    if dy == 0:
        if dx > 0: return (1, 0)
        else: return (-1, 0)

    # ok, with that out of the way...
    low = min(abs(dx), abs(dy))
    origX = dx
    origY = dy

    if dx < 0: dx *= -1
    if dy < 0: dy *= -1

    divisor = gcd(dx, dy)
    dx = int(dx / divisor)
    dy = int(dy / divisor)

    if origX < 0: dx *= -1
    if origY < 0: dy *= -1

    return (dx, dy)
# }}}


def greaterThan(a, b, c):
# {{{
    """
    given a center point `c` around which everything revolves,
    determine whether or not point a is greater than
    (should appear after/to the right of) point b

    >>> greaterThan( (1,1), (3,3), (2,2) )
    False
    >>> greaterThan( (1,1), (2,1), (2,2) )
    False
    >>> greaterThan( (2,0), (2,1), (2,2))
    True
    """
    if a[0] - c[0] >= 0 and b[0] - c[0] < 0:
        return True
    if a[0] - c[0] < 0 and b[0] - c[0] >= 0:
        return False
    if a[0] - c[0] == 0 and b[0] - c[0] == 0:
        if a[1] - c[1] >= 0 or b[1] - c[1] >= 0:
            return a[1] > b[1]
        return b[1] > a[1]
    det = ((a[0] - c[0]) * (b[1] - c[1])) - ((b[0] - c[0]) * (a[1] - c[1]))
    if det < 0:
        return True
    if det > 0:
        return False
    d1 = ((a[0] -  c[0]) * (a[0] - c[0])) + ((a[1] - c[1]) * (a[1] - c[1]))
    d2 = ((b[0] -  c[0]) * (b[0] - c[0])) + ((b[1] - c[1]) * (b[1] - c[1]))
    return d1 > d2
# }}}


class Asteroid(object):
    def __init__(self, x, y, center):
        self._x = x
        self._y = y
        self._center = center
        self._calculateIncline()

    def __str__(self):
        return "Asteroid<({},{}),d={},s=({},{}),q={}>".format(
            self._x, self._y, self.distance(),
            self._incline[0], self._incline[1],
            self.quadrant()
        )
    def __repr__(self):
        return self.__str__()

    def distance(self):
        return manhattan((self._x, self._y), self._center)

    def _calculateIncline(self):
    # {{{
        dx = abs(self._x - self._center[0])
        dy = abs(self._y - self._center[1])
        divisor = gcd(dx, dy)
        dx = int(dx / divisor)
        dy = int(dy / divisor)
        self._incline = (dx, dy)
    # }}}

    def incline(self):
        return self._incline

    def quadrant(self):
    # {{{
        if self._x == self._center[0]:
            # N or S
            if self._y < self._center[1]:
                return 'N'
            return 'S'
        if self._y == self._center[1]:
            # E or W
            if self._x < self._center[0]:
                return 'W'
            return 'E'
        if self._y < self._center[1]:
            # N...
            if self._x < self._center[0]:
                return 'NW'
            return 'NE'
        else:
            # S...
            if self._x < self._center[0]:
                return 'SW'
            return 'SE'
    # }}}

    def coord(self):
        return (self._x, self._y)

    def __eq__(self, other):
        return self.incline() == other.incline()

    def __lt__(self, other):
        return greaterThan(
            other.coord(),
            self.coord(),
            self._center
        )



class Moon(object):
    def __init__(self, x, y, z, vx=0, vy=0, vz=0, num=None):
        self._position = {'x': x, 'y': y, 'z': z}
        self._velocity = {'x': vx, 'y': vy, 'z': vz}
        self._initialConfiguration = ( tuple(self._position.items()), tuple(self._velocity.items()))
        self._num = num

    def getPos(self, axis):
        return self._position[axis]

    def getVelocity(self, axis):
        return self._velocity[axis]

    def calculateVelocity(self, influencers):
        # uglyhack, since calcVel is the first op for each new iteration,
        # we add the old (previous iterations) position to the set of
        # known positions, BEFORE we do something for this current
        # iteration

        forces = defaultdict(list)

        for axis in self._velocity.keys():
            ourPos = self.getPos(axis)
            for moon in influencers:
                if moon == self:
                    continue
                theirPos = moon.getPos(axis)
                if ourPos < theirPos:
                    forces[axis].append(1)
                elif ourPos > theirPos:
                    forces[axis].append(-1)
                else:
                    forces[axis].append(0)

        for axis in forces.keys():
            self._velocity[axis] += sum(forces[axis])



    def applyVelocity(self):
        for axis in self._position.keys():
            self._position[axis] += self._velocity[axis]

    def potential(self):
        return sum(map(abs, self._position.values()))

    def kinetic(self):
        return sum(map(abs, self._velocity.values()))

    def total(self):
        return self.potential() * self.kinetic()

    def atInitialConfiguration(self):
        return (tuple(self._position.items()), tuple(self._velocity.items())) == self._initialConfiguration

    def atInitialConfigurationOnAxis(self, axis):
        initialPos = self._initialConfiguration[0]
        for p in initialPos:
            if p[0] == axis:
                return self._position[axis] == p[1]

    def __str__(self):
        return "Moon<{}>".format(
            '[Unknown]' if self._num is None else self._num
        )
    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

# vim: set ft=python foldmethod=marker :
