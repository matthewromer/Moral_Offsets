#sqDistWrapper Creates a normal or lognormal squiggle distribution

import squigglepy as sq

def sqDistWrapper(dist,fifth,nintyfifth):
    if dist == 'norm':
        out = sq.norm(x=fifth,y=nintyfifth)
    elif dist == 'lognorm':
        out = sq.lognorm(x=fifth,y=nintyfifth)
    
    return out