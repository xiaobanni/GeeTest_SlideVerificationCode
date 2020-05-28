# -*- coding: utf-8 -*-

import numpy as np
import math

c1 = 1.70158
c2 = c1 * 1.525
c3 = c1 + 1
c4 = ( 2 * math.pi ) / 3
c5 = ( 2 * math.pi ) / 4.5

def ease_in_quad(x):
    return x * x

def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)

def ease_in_out_quad(x):
    if(x<0.5):
        return 2*x*x
    else:
        return 1-pow(-2 * x +2 , 2) / 2

#-----------------------------------------------

def ease_in_cubic(x):
    return x * x * x

def ease_out_cubic(x):
    return 1 - pow( 1-x, 3)

def ease_in_out_cubic(x):
    if x < 0.5:
        return 4 * x * x * x
    else:
        return 1 - pow( -2 * x + 2, 3 ) / 2

#-----------------------------------------------

def ease_in_quart(x):
    return x * x * x * x

def ease_out_quart(x):
    return 1 - pow(1 - x, 4)

def ease_in_out_quart(x):
    if x < 0.5:
        return 8 * x * x * x * x
    else:
        return 1 - pow( -2 * x + 2, 4 ) / 2

#-----------------------------------------------

def ease_in_quint(x):
    return  x * x * x * x * x

def ease_out_quint(x):
    return 1 - pow( 1 - x, 5 )

def ease_in_out_quint(x):
    if x < 0.5:
        return 16 * x * x * x * x * x
    else:
        return 1 - pow( -2 * x + 2, 5 ) / 2

#-----------------------------------------------

def ease_in_sine(x):
    return 1 - math.cos( x * math.pi/2 )

def ease_out_sine(x):
    return math.sin( x * math.pi/2 )

def ease_in_out_sine(x):
    return -( math.cos( math.pi * x ) - 1 ) / 2

#------------------------------------------------

def ease_in_expo(x):
    if x==0:
        return 0
    else:
        return pow( 2, 10 * x - 10)

def ease_out_expo(x):
    if x == 1:
        return 1
    else:
        return 1 - pow(2, -10 * x)

def ease_in_out_expo(x):
    if x==0:
        return 0
    else:
        if x==1:
            return 1
        else:
            if x<0.5:
                return pow( 2, 20 * x - 10 ) / 2
            else:
                return ( 2 - pow( 2, -20 * x + 10 ) ) / 2

#---------------------------------------------------------

def ease_in_cric(x):
    return 1 - math.sqrt( 1 - pow( x, 2 ) )

def ease_out_cric(x):
    return math.sqrt( 1 - pow( x - 1, 2 ) )

def ease_in_out_cric(x):
    if x < 0.5:
        return ( 1 - math.sqrt( 1 - pow( 2 * x, 2 ) ) ) / 2
    else:
        return ( math.sqrt( 1 - pow( -2 * x + 2, 2 ) ) + 1 ) / 2

#-----------------------------------------------------------------

def ease_in_bounce(x):
    return 1 - ease_out_bounce( 1-x )

def ease_out_bounce(x):
    n1 = 7.5625
    d1 = 2.75
    if x < 1 / d1 :
        return n1 * x * x
    elif x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x*x + 0.75
    elif x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x*x + 0.9375
    else:
        x -= 2.625 / d1
        return n1 * x*x + 0.984375

def ease_in_out_bounce(x):
    if x<0.5:
        return (1 - ease_out_bounce(1- 2 * x ) ) / 2
    else:
        return (1 + ease_out_bounce(2 * x -1 ) ) / 2
#-----------------------------------------------

def ease_in_elastic(x):
    if x==0:
        return 0
    else:
        if x==1:
            return 1
        else:
            return -pow( 2, 10 * x - 10 ) * math.sin( ( x * 10 - 10.75 ) * c4 )

def ease_out_elastic(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1

def ease_in_out_elastic(x):
    if x==0:
        return 0
    else:
        if x==1:
            return 1
        else:
            if x <0.5:
                return -( pow( 2, 20 * x - 10 ) * math.sin( ( 20 * x - 11.125 ) * c5 )) / 2
            else:
                return pow( 2, -20 * x + 10 ) * math.sin( ( 20 * x - 11.125 ) * c5 ) / 2 + 1

#---------------------------------------------------------------

def ease_in_back(x):
    return c3 * x * x * x - c1 * x * x

def ease_out_back(x):
    return 1 + c3 * pow( x - 1, 3 ) + c1 * pow( x - 1, 2 )

def ease_in_out_back(x):
    if x<0.5:
        return ( pow( 2 * x, 2 ) * ( ( c2 + 1 ) * 2 * x - c2 ) ) / 2
    else:
        return ( pow( 2 * x - 2, 2 ) *( ( c2 + 1 ) * ( x * 2 - 2 ) + c2 ) + 2 ) / 2

#-------------------------------------------------------------


def get_tracks(distance, seconds, ease_func):
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        ease = globals()[ease_func]
        offset = round(ease(t/seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)

    return offsets, tracks
