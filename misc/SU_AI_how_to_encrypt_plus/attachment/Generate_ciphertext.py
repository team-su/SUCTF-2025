import torch
import torch.nn as nn
flag=''
flag_list=[]
for i in flag:
    binary_str = format(ord(i), '09b')
    print(binary_str)
    for bit in binary_str:
        flag_list.append(int(bit))
input=torch.tensor(flag_list, dtype=torch.float32)
n=len(flag)
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.linear = nn.Linear(n, n*n)
        self.conv=nn.Conv2d(1, 1, (2, 2), stride=1,padding=1)
        self.conv1=nn.Conv2d(1, 1, (3, 3), stride=3)

    def forward(self, x):
        x = x.view(1,1,3, 3*n)
        x = self.conv1(x)
        x = x.view(n)
        x = self.linear(x)
        x = x.view(1, 1, n, n)
        x=self.conv(x)
        return x
mynet=Net()
mynet.load_state_dict(torch.load('model.pth'))
output=mynet(input)
with open('ciphertext.txt', 'w') as f:
    for tensor in output:
        for channel in tensor:
            for row in channel:
                f.write(' '.join(map(str, row.tolist())))
                f.write('\n')