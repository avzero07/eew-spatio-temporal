import pytest
import torch
import numpy as np
import matplotlib.pyplot as plt

from est_lib.nn.common import *

# Helper Function
def gen_sig_fig8_type1(sin_scale,sin_t_pow,cos_scale,
        cos_t_pow,t=torch.from_numpy(np.linspace(0,2,1000))):
    pi = torch.arccos(torch.zeros(1))*2
    exp = torch.exp(-1*torch.square(t))
    sin = torch.sin(sin_scale*pi*torch.pow(t,sin_t_pow))
    cos = torch.cos(cos_scale*pi*torch.pow(t,cos_t_pow))
    sig = exp * sin * cos
    return sig.double()
    
def gen_sig_fig8_type2(exp_scale,sin_scale,sin_exp_t_scale,
        t=torch.from_numpy(np.linspace(0,2,1000))):
    pi = torch.arccos(torch.zeros(1))*2
    exp = torch.exp(-1*t)
    sin = torch.sin(sin_scale*pi*t*torch.exp(t*sin_exp_t_scale))
    sin2 = torch.sin(0.5 * pi * t)
    sig = exp_scale * exp * sin * sin2
    return sig.double()

# Start Tests

@pytest.mark.parametrize(
        "ip,op",
        [((1,0),(0,0,0)),
         ((0.75,0.628),(-0.1996,0.1992,0.2499))])
def test_russell(ip,op):
    '''
    Test corresponding to Figure 4 in Russell's paper
    '''
    pi = torch.arccos(torch.zeros(1))*2
    phi = ip[1]
    a = ip[0]
    t = torch.from_numpy(np.linspace(0,1,1000))
    sigA = a * torch.exp(-1*t)*torch.sin((40*pi*t)+phi)
    sigB = torch.exp(-1*t)*torch.sin(40*pi*t)

    '''
    plt.figure()
    plt.plot(t,sigA,label='sigA')
    plt.plot(t,sigB,label='sigB')
    plt.xticks(np.arange(0,0.2,step=0.02))
    plt.grid()
    plt.axis([0,0.2,-2,2])
    plt.show()
    '''

    em,ep,ec = russell_error(sigA,sigB)
    print("em={:.4f},ep={:.4f},ec={:.4f}".format(em.item(),ep.item()
                                                ,ec.item()))
    if (phi==0) and (a==1):
        assert em == 0, "Check Error Computation!"
        assert ep == 0, "Check Error Computation!"
        assert ec == 0, "Check Error Computation!"
    else:
        tem = torch.tensor(op[0]).double()
        tep = torch.tensor(op[1]).double()
        tec = torch.tensor(op[2]).double()
        assert torch.isclose(em,tem,atol=0.01), "Check Error Computation!"
        assert torch.isclose(ep,tep,atol=0.01), "Check Error Computation!"
        assert torch.isclose(ec,tec,atol=0.01), "Check Error Computation!"

@pytest.mark.parametrize(
        "ip,op",
        [((gen_sig_fig8_type1(3,0.5,1.1,2),gen_sig_fig8_type1(3.3,0.5,1,2))
            ,(-0.0147,0.1932,0.1717)),
         ((gen_sig_fig8_type2(1.5,4.35,-0.12),gen_sig_fig8_type2(2,5,-0.2)),
             (-0.1995,0.2127,0.2584))])
def test_russell_alter(ip,op):
    '''
    Test corresponding to Figure 8 in Russell's paper
    '''
    sigA = ip[0] 
    sigB = ip[1] 
    em,ep,ec = russell_error(sigA,sigB)
    print("em={:.4f},ep={:.4f},ec={:.4f}".format(em.item(),ep.item()
                                                ,ec.item()))
    tem = torch.tensor(op[0]).double()
    tep = torch.tensor(op[1]).double()
    tec = torch.tensor(op[2]).double()
    assert torch.isclose(em,tem,atol=0.0001), "Check Error Computation!"
    assert torch.isclose(ep,tep,atol=0.0001), "Check Error Computation!"
    assert torch.isclose(ec,tec,atol=0.0001), "Check Error Computation!"

    '''
    plt.figure()
    plt.plot(t,sigA,label='sigA')
    plt.plot(t,sigB,label='sigB')
    plt.xticks(np.arange(0,2,step=0.25))
    plt.grid()
    plt.axis([0,2,-1,1.25])
    plt.show()
    '''

