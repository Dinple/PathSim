import numpy as np


def diffusion(M_, intens=0.05, regularize=True):
    M_ = M_.copy()
    r_add = intens * np.roll(M_, shift=1, axis=1)
    r_add[:, 0] = 0
    l_add = intens * np.roll(M_, shift=-1, axis=1)
    l_add[:, -1] = 0
    d_add = intens * np.roll(M_, shift=1, axis=0)
    d_add[0, :] = 0
    u_add = intens * np.roll(M_, shift=-1, axis=0)
    u_add[-1, :] = 0

    M_ += r_add + l_add + d_add + u_add
    
    if regularize:
        # any value > 1 is set to 1
        M_[M_ > 1] = 1
        
    return M_


def diffuse(M_, d=0.5):
    contrib = M_ * d
    w = contrib / 8.0
    r = M_ - contrib
    N = np.roll(w, shift=-1, axis=0)
    S = np.roll(w, shift=1, axis=0)
    E = np.roll(w, shift=1, axis=1)
    W = np.roll(w, shift=-1, axis=1)
    NW = np.roll(N, shift=-1, axis=1)
    NE = np.roll(N, shift=1, axis=1)
    SW = np.roll(S, shift=-1, axis=1)
    SE = np.roll(S, shift=1, axis=1)
    diffused = r + N + S + E + W + NW + NE + SW + SE
    return diffused
