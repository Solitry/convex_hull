from typing import List

import torch
from torch.nn.parameter import Parameter
from torch.nn import functional as F
from torch.nn import Module
from torch.nn import init
import numpy as np

from common.value_type import Line


class ConvexNet(Module):

    __constants__ = ['width']

    def __init__(self, width):
        super(ConvexNet, self).__init__()

        self.width = width
        self.weight = Parameter(torch.Tensor(2, width))
        self.bias = Parameter(torch.Tensor(width))

    def set_value(self, lines: List[Line]):
        assert len(lines) == self.width

        weight = [[], []]
        bias = []

        for line in lines:
            weight[0].append(line.a)
            weight[1].append(line.b)
            bias.append(line.c)
        
        self.weight = Parameter(torch.Tensor(weight))
        self.bias = Parameter(torch.Tensor(bias))
    
    def get_value(self) -> List[Line]:
        ret = []
        weight_list = self.weight.tolist()
        bias_list = self.bias.tolist()

        for i in range(self.width):
            ret.append(Line(weight_list[0][i], weight_list[1][i], bias_list[i]))
        
        return ret

    def forward(self, input):
        length2 = torch.sum(self.weight.mul(self.weight), dim=0)
        length = torch.sqrt(length2)

        approx_dis = torch.addmm(self.bias, input, self.weight)
        real_dis = torch.div(approx_dis, length)

        max_dis, _ = torch.max(real_dis, dim=1)
        ret = torch.sigmoid(max_dis * 1e2)

        # print(real_dis)
        # print(max_dis)
        # print(ret)

        return ret
        

if __name__ == '__main__':
    w = torch.randn(2, 4)
    print(w)

    w2 = w ** 2
    print(w2)

    l2 = torch.sum(w2, dim=0)
    print(l2)

    l = torch.sqrt(l2)
    print(l)

    d = torch.div(w, l)
    print(d)

    b = torch.sum(d, dim=1)
    print(b)

    print(b[0].item(), b[1].item())
