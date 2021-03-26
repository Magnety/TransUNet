from torch import nn
from .BackBone.ResNeXt3D import ResNeXt3D
from .BackBone.ResNeXt3D import ResNeXtBottleneck
from .BackBone.SENet import SENet,SEResNeXtBottleneck,se_resnext50_32x4d


class BackBone3D(nn.Module):
    def __init__(self):
        super(BackBone3D, self).__init__()
        #net = ResNeXt3D(ResNeXtBottleneck, [3, 4, 6, 3], num_classes=2)
        net = se_resnext50_32x4d(num_classes=2,pretrained=None)
        # resnext3d-101 is [3, 4, 23, 3]
        # we use the resnet3d-50 with [3, 4, 6, 3] blocks
        # and if we use the resnet3d-101, change the block list with [3, 4, 23, 3]

        net = list(net.children())
        print("net.shape")
        print(len(net))
        print(net)
        print("--------------------------------------------")
        print(net[5])

        self.layer0 = nn.Sequential(*net[:1])
        # the layer0 contains the first convolution, bn and relu
        self.layer1 = nn.Sequential(*net[1:2])
        # the layer1 contains the first pooling and the first 3 bottle blocks
        self.layer2 = net[2]
        # the layer2 contains the second 4 bottle blocks
        self.layer3 = net[3]
        # the layer3 contains the media bottle blocks
        # with 6 in 50-layers and 23 in 101-layers
        self.layer4 = net[4]
        # the layer4 contains the final 3 bottle blocks
        # according the backbone the next is avg-pooling and dense with num classes uints
        # but we don't use the final two layers in backbone networks

    def forward(self, x):
        layer0 = self.layer0(x)
        layer1 = self.layer1(layer0)
        layer2 = self.layer2(layer1)
        layer3 = self.layer3(layer2)
        layer4 = self.layer4(layer3)
        return layer4
