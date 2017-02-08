import math
# pragma pylint: disable=bad-whitespace

_a = math.pow(2, 1.0/12)
A  = 440
As = A * _a; Bf = As
B  = A * math.pow(_a, 2)
C  = A * math.pow(_a, 3)
Cs = A * math.pow(_a, 4); Df = Cs
D  = A * math.pow(_a, 5)
Ds = A * math.pow(_a, 6); Ef = Ds
E  = A * math.pow(_a, 7)
F  = A * math.pow(_a, 8)
Fs = A * math.pow(_a, 9); Gf = Fs
G  = A * math.pow(_a, 10)
Gs = A * math.pow(_a, 11); Af = Gs

class octave:
    up = math.pow(_a, 12)
    down = math.pow(_a, -12)

class scores(object):
    lamb = [0.2,
            E, D, C, D,
            E, E, E, None,
            D, D, D, None,
            E, G, G, None,
            E, D, C, D,
            E, E, E, E,
            D, D, E, D,
            C, None, C*octave.up, None]
    
    birthday = [0.1, C, C, D, None,
                C, None, F, None, E, None, None,
                C, C, D, None,
                C, None, G, None, F, None, None,
                C, C, C*octave.up, None, A*octave.up, None,
                F, None, E, None, D, None, None,
                Bf*octave.up, Bf*octave.up, A*octave.up, None,
                F, None, G, None, F]
    
    error      = [0.1, C, C, C]
    connect    = [0.1, C, G]
    disconnect = [0.1, G, C]
    critical   = [0.2,
                  C, G*octave.down, None,
                  C, G*octave.down, None]
