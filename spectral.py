import numpy as np
import logger
import scipy


def get_max_token_id(token_lists):
    return max([x[0] for sublist in token_lists for x in sublist])

def expand_token(token, V):
    vec = np.array([0]*V)
    vec[token[0]] = 1
    return vec

def get_M1(token_lists, V):
    tls_np = np.array(token_lists)
    D = tls_np.shape[0]
    L = tls_np.shape[1]
    M1 = np.array([0]*V)
    for d in range(D):
        for l in range(L):
            M1 += expand_token(tls_np[d,l,:], V)
    return M1 / (D*L)

def get_M2(token_lists, V, M1, alphas):
    alpha0 = alphas.sum()
    tls_np = np.array(token_lists)
    sum_of_outers = np.array(0, shape=(V,V))
    for d in range(D):
        for l1 in range(L):
            for l2 in range(L):
                if l1 != l2:
                    sum_of_outers += np.outer(expand_token(tls_np[d, l1, :], V), expand_token(tls_np[d, l2, :], V))
    M1_outer = alpha0/(alpha0+1)*np.outer(M1, M1)
    return sum_of_outers - M1_outer

def get_sv1(M2):
    return np.linalg.svd(M2, compute_uv=False)[0]

def deltaprime(K, d2, d3, V, beta):
    numer = np.log(K/d3)*K*(beta + 2*np.log(K/d2))**2
    denom = V*beta
    return np.sqrt(numer/denom)

def get_sigbar1(K, d1, d2, d3, V, beta, alphas):
    a_max = max(alphas)
    a_0 = alphas.sum()
    a_frac = a_max/(a_0*(a_0 + 1))
    numer = (1 + deltaprime(K, d2, d3, V, beta))*V*(beta + K*beta**2)
    denom = (V*beta - np.sqrt(2*V*beta*np.log(K/d1)))**2
    return a_frac*numer/denom


def get_lower_bound(delta, D, L, V):
    """delta: bound error, D: num_docs, L: words per doc, V: vocab size"""
    scale = 1./np.sqrt(D*delta)
    factor = np.sqrt(2*L**(-2) + 2*V**(-2))
    return scale*factor

def get_upper_bound(K_guess, d1, d2, d3, V, beta, alphas):
    func = lambda K : get_sigbar1(K, d1, d2, d3, V, beta, alphas)
    try:
        return scipy.optimize.fsolve(func, K_guess)
    except:
        logger.warning("Unable to solve for K. Setting upper bound to 1000.")
        return 1000



