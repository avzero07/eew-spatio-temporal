'''
Simple Model for the CP-Line Equivalent
'''

import torch
import torch.nn as nn
import torch.nn.functional as F

class cp_line_simple(nn.Module):
    def __init__(self):
        super(cp_line_simple, self).__init__()

    def forward(self,x):
        return x
