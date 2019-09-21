

def im_col32(b, g, r, a=0xff):
    return (a << 24) | (b << 16) | (g << 8) | (r << 0)
