import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):

    def __init__(self):
#Python中 __init__的通俗解释是什么？ - 知乎
#https://www.zhihu.com/question/46973549/answer/103805810
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 3x3 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 3)#nn.Conv2d(in_channels, out_channels, kernel_size)
        self.conv2 = nn.Conv2d(6, 16, 3)
        # an affine operation: y = Wx + b
        #https://www.jianshu.com/p/45a26d278473
        self.fc1 = nn.Linear(16 * 6 * 6, 120)  #nn.Linear(in_channels,out_channels)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


net = Net()
print("net = \n")
print(net)


params = list(net.parameters())
print(len(params))
print("conv1's weight = ")
print(params[0].size())  # conv1's weight
print("conv1's bias = ")
print(params[1].size())  # conv1's bias
print("Linear3's weight = ")
print(params[8].size())  # Linear3's weight
print("Linear3's bias = ")
print(params[9].size())  # Linear3's bias

input = torch.randn(1, 1, 32, 32)
out = net(input)
print("out = ")
print(out)


output = net(input)
target = torch.randn(10)  # a dummy target, for example
target = target.view(1, -1)  # make it the same shape as output
criterion = nn.MSELoss()

loss = criterion(output, target)
print("loss  = ")
print(loss)

print("loss.grad_fn = ")
print(loss.grad_fn)  # MSELoss
print("loss.grad_fn.next_functions[0][0] = ")
print(loss.grad_fn.next_functions[0][0])  # Linear
print("loss.grad_fn.next_functions[0][0].next_functions[0][0] =")
print(loss.grad_fn.next_functions[0][0].next_functions[0][0])  # ReLU


print('conv1.bias.grad before zero_grad() = ')
print(net.conv1.bias.grad)

net.zero_grad()     # zeroes the gradient buffers of all parameters

print('conv1.bias.grad before backward = ')
print(net.conv1.bias.grad)

loss.backward()

print('conv1.bias.grad after backward = ')
print(net.conv1.bias.grad)

#backward() https://www.cnblogs.com/luckyscarlett/p/10552747.html


import torch.optim as optim

# create your optimizer
optimizer = optim.SGD(net.parameters(), lr=0.01)

# in your training loop:
optimizer.zero_grad()   # zero the gradient buffers
# This is because gradients are accumulated as explained in the Backprop section.
output = net(input)
loss = criterion(output, target)
loss.backward()
optimizer.step()    # Does the update

