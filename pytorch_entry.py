import torch
import math

from net.convex_net import ConvexNet
from common.value_type import Line


if __name__ == '__main__':
    # net = ConvexNet(4)
    # net.set_value([
    #     Line(1, 1, -1),
    #     Line(1, -1, -0.5),
    #     Line(-1, 1, -0.5),
    #     Line(0, -1, 0.5),
    # ])

    # input = torch.Tensor([
    #     [0.2, 0.2],
    #     [0.8, 0.8],
    #     [0.8, 0.2],
    #     [0.2, 0.8],
    #     [0.1, 0.9],
    #     [0.1, 0.1],
    #     [0.9, 0.1],
    #     [0.9, 0.9],
    #     [0.28, 0.56],
    # ])

    # target = torch.Tensor([
    #     0,
    #     0,
    #     0,
    #     0,
    #     1,
    #     1,
    #     1,
    #     1,
    #     0,
    # ])

    # # print(input, input.size())
    # # print(target, target.size())

    # optimizer = torch.optim.SGD(net.parameters(), lr=0.1, momentum=0.9)
    # loss_fn = torch.nn.MSELoss()

    # for _ in range(20):
    #     optimizer.zero_grad()
    #     output = net(input)
    #     loss = loss_fn(output, target)
    #     print(loss)
    #     loss.backward()
    #     optimizer.step()

    # a = torch.rand(2)
    # print(a)
    
    # v = a.tolist()
    # print(v)

    # a = torch.Tensor([0.324, 0.5001, 0.6867, 0.111])
    # b = torch.Tensor([0, 1, 1, 0])

    # ar = torch.round(a)
    # c = (ar == b)
    # print(c)
    # cf = c.float()
    # print(cf)
    # print(cf.mean())

    out_features = 4
    in_features = 2

    weight = torch.Tensor(out_features, in_features)
    bias = torch.Tensor(out_features)
    # weight = torch.nn.parameter.Parameter(torch.Tensor(out_features, in_features))
    # bias = torch.nn.parameter.Parameter(torch.Tensor(out_features))

    torch.nn.init.kaiming_uniform_(weight, a=math.sqrt(0))
    fan_in, _ = torch.nn.init._calculate_fan_in_and_fan_out(weight)
    bound = 1 / math.sqrt(fan_in)
    torch.nn.init.uniform_(bias, -bound, bound)

    print(weight)
    print(bias)
    print(weight.tolist())
    print(bias.tolist())
