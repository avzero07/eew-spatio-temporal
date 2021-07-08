'''
Simple Model for the CP-Line Equivalent
'''

import torch
import torch.nn as nn
import torch.nn.functional as F

class cp_line_simple(nn.Module):
    def __init__(self,num_in_nodes=2,
                 feat_size=1,hidden=3):
        # feat_size for ip and op
        super(cp_line_simple, self).__init__()
        self.num_in_nodes = num_in_nodes
        self.feat_size = feat_size
        self.hidden_size = hidden

        # Layer Definitions

        # One LSTM per Input Node
        self.lstms = nn.ModuleList()
        for n in range(num_in_nodes):
            lstm = nn.LSTM(input_size=feat_size,
                           hidden_size=feat_size,
                           num_layers=1,
                           bias=True,
                           batch_first=True,
                           dropout=0,
                           bidirectional=False,
                           proj_size=0)
            self.lstms.append(lstm)

        # Linear Layer[s] for OP
        # Per feature basically
        self.hidden = nn.ModuleList()
        for l in range(feat_size):
            self.hidden.append(nn.Linear(in_features=num_in_nodes,
                                out_features=hidden))
        self.op = nn.ModuleList()
        for l in range(feat_size):
            self.op.append(nn.Linear(in_features=hidden,
                                out_features=1))
        # Potentially, any softmax type of thing goes here

    def forward(self,x):
        # input -> batch x seq x nodes x features
        x_list = list()
        for i,layer in enumerate(self.lstms):
            # Slice Here
            temp = x[:,:,i,:]
            temp,(hn_temp,cn_temp) = self.lstms[i](temp)
            # hn_temp = temp[:,-1,:]
            hn_temp = torch.squeeze(hn_temp,dim=0)
            # assert hn_temp.shape == temp[:,-1,:].shape
            x_list.append(hn_temp) # Use last output only

        # init op_list
        result = list()

        for l in range(self.feat_size):
            tens_temp = list()
            for n in range(self.num_in_nodes):
                tens_temp.append(x_list[n][:,l])
            x_temp = torch.stack(tens_temp,-1)
            # Op at Hidden
            inter = torch.tanh(self.hidden[l](x_temp))
            result.append(self.op[l](inter))
        '''
        There will need to be as many losses as output length
        in result. (up to 3)

        These losses will have to be combined before calling
        backward().

        Eg:
            loss1 = criterion(outEW,realEW)
            loss2 = criterion(outNS,realNS)
            loss3 = criterion(outUD,realUD)
            loss = torch.add(loss1,loss2,loss3)

            loss.backward()
            optimizer.step()
        '''
        return result
