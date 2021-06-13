'''
Contains utilities and functions commonly utilized across nn models
'''

import torch

def russell_error(sigA,sigB):
    '''
    Implementation of the error measure proposed by David M. Russell
    in 
    Russell, D.M. (1997b), 
        “Error Measures for Comparing Transient Data: Part II: Error
        Measures Case Study”, 
        68th Shock and Vibration Symposium, Hunt Valley, MD, pp. 185 – 198

    '''
    # Batch Length should be the same (corresponds to sequence length)
    assert sigA.shape[0] == sigB.shape[0], "Batch Length Mismatch!"

    pi = torch.arccos(torch.zeros(1))*2

    # Mag Measure

    # Component A,B => Sum of Squares
    A = torch.sum(torch.square(sigA))
    B = torch.sum(torch.square(sigB))
    rootAB = torch.sqrt(A*B)

    m = (A - B)/rootAB

    # Phase Measure

    # Component C => Correl Equivalent
    C = torch.sum(sigA*sigB)

    p = C/rootAB

    # Compute Error Measures
    em = torch.sign(m)*torch.log10(1+torch.abs(m))
    ep = torch.arccos(p)/pi
    ec = torch.sqrt((pi/4)*(torch.square(em)+torch.square(ep)))
    return em.double(),ep.double(),ec.double()
