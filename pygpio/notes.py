import math
# pragma pylint: disable=bad-whitespace
# pragma: no cover

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
rest = None; _ = None

class octave:
    up = math.pow(_a, 12); u = up
    down = math.pow(_a, -12); d = down
oc = octave

class scores(object):
    lamb = [0.2,
            E, D, C, D, E, E, E, _,
            D, D, D, _, E, G, G, _,
            E, D, C, D, E, E, E, E,
            D, D, E, D, C, _, C*oc.u, _]
    
    birthday = [0.1, C, C, D, _, C, _, F, _, E, _, _,
                     C, C, D, _, C, _, G, _, F, _, _,
                     C, C, C*oc.u, _, A*oc.u, _, F, _, E, _, D, _, _,
                     Bf*oc.u, Bf*oc.u, A*oc.u, _, F, _, G, _, F]
    
    mario = [0.1, E, E, _, E, _, C, E, _, G, _, _, _, G*oc.d, _, _, _]
    mario_2 = [0.1, C, _, _, G*oc.d, _, _, E*oc.d, _, A, _, B, _, Bf, A, _,
                    G*oc.d, E, G, A*oc.u, _, F, G, _, E, _, C, D, B, _, _, _]
    mario_3 = [0.1, G, Gf, F, Ds, _, E, _, Gs*oc.d, A, C, _, A, C, D, _, _]
    mario_4 = [0.1, G, Gf, F, Ds, _, E, _, C*oc.u, _, C*oc.u, C*oc.u, _, _, _]
    mario_5 = [0.1, Ef, _, _, D, _, _, C, _, _, _, _, _, _]
    
    mario_full = mario + mario_2[1:] + mario_2[1:] + mario_3[1:] + mario_4[1:] + mario_3[1:] + mario_5[1:] +\
                 mario_3[1:] + mario_4[1:] + mario_3[1:] + mario_5[1:]
    
    star_1 = [0.1, D*oc.d, D*oc.d, D*oc.d, G*oc.d, _, _, _, _, D, _, _, _, _]
    star_2 = [0.1, C, B, A, G, _, _, _, _, D, _, _]
    star_3 = [0.1, C, B, C, A, _, _, _, _]
    star_4 = [0.1, D*oc.d, _, D*oc.d, G*oc.d, _, _, _, _, D, _, _, _]
    
    star_wars = star_1 + star_2[1:] + star_2[1:] + star_3[1:] + star_4[1:] + star_2[1:] + star_2[1:] + star_3[1:]
    
    all_star_1 = [0.2, Fs*oc.d, _, Cs, As, As, _, Gs*oc.d, Fs*oc.d, Fs*oc.d, B, _, As, As, Gs*oc.d, Gs*oc.d, Fs*oc.d, _]
    all_star_2 = [0.2, Fs*oc.d, Cs, As, As, Gs*oc.d, Gs*oc.d, Fs*oc.d, Fs*oc.d, Ds*oc.d, _, Cs*oc.d, _, _, _]
    all_star_3 = [0.2, Fs*oc.d, Fs*oc.d, Cs, As, As, Gs*oc.d, Gs*oc.d, Fs*oc.d, Fs*oc.d, B, _, As, As, Gs*oc.d, Gs*oc.d, Fs*oc.d, Fs*oc.d]
    all_star_4 = [0.2, Cs, _, As, As, Gs*oc.d, _, Fs*oc.d, Fs*oc.d, Gs*oc.d, _, Ds*oc.d, _, _, _]
    
    all_star = all_star_1 + all_star_2[1:] + all_star_3[1:] + all_star_4[1:]
    
    thrones_1 = [0.1, G, _, C, _, Ef, F]
    thrones_2 = [0.1, G, _, C, _, E, F]
    thrones_intro = [0.1] + thrones_1[1:] + thrones_1[1:] + thrones_1[1:] + thrones_2[1:] \
                + thrones_2[1:] + thrones_2[1:] + thrones_2[1:] + thrones_2[1:]
    
    thrones_3 = [0.1, G, _, _, _, _, C, _, _, _, Ef, F, G, _, _, _, C, _, _, _, Ef, F]
    thrones_4 = [0.1, D, _, F*oc.d, _, Bf, C]
    thrones_5 = [0.1, F, _, _, _, _, Bf, _, _, _, Ef, D, F, _, _, _, Bf, _, _, _, Ef, D]
    thrones_6 = [0.1, C, _, G*oc.d, _, A, Bf]
    thrones_7 = [0.1, F, _, _, _, _, Bf, _, _, _, D, _, _, Ef, _, _, D, _, _, Bf, _]
    
    thrones_full = thrones_intro \
                + thrones_3[1:] + thrones_4[1:] + thrones_4[1:] + thrones_4[1:] + thrones_4[1:] \
                + thrones_5[1:] + thrones_6[1:] + thrones_6[1:] + thrones_6[1:] + thrones_6[1:] \
                + thrones_3[1:] + thrones_4[1:] + thrones_4[1:] + thrones_4[1:] + thrones_4[1:] \
                + thrones_7[1:] + thrones_6[1:] + thrones_6[1:] + thrones_6[1:] + thrones_6[1:] + [C]
                


if __name__ == "__main__": # pragma: no cover
    import sys
    from pygpio import Gpio, modes
    
    g = Gpio()
    p = g.setup(18, modes.PWM)
    p.playScore(scores.__dict__[sys.argv[1]])
