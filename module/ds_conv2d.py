# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
from torchinfo import summary


class DSConv2d(nn.Module):
    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        stride,
        padding,
    ):
        super().__init__()

        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

        self.depthwise_conv2d = nn.Conv2d(
            self.in_channels,
            self.in_channels,
            kernel_size=self.kernel_size,
            stride=self.stride,
            padding=self.padding,
            groups=self.in_channels,
        )
        self.pointwise_conv2d = nn.Conv2d(
            self.in_channels,
            self.out_channels,
            kernel_size=1,
        )

        self.apply(self.weight_init)

    def weight_init(self, m):
        if isinstance(m, nn.Conv2d):
            nn.init.normal_(m.weight.data, std=0.05)
            nn.init.constant_(m.bias.data, 0.0)

    def forward(self, X):
        # X [B, C, F, T]
        Y = self.depthwise_conv2d(X)
        Y = self.pointwise_conv2d(Y)
        # [B, C, F, T]
        return Y


if __name__ == "__main__":
    print(f"Test DSConv2d Module Start...")

    # get model
    model = DSConv2d(2, 16, kernel_size=(5, 2), stride=(2, 1), padding=(2, 1))
    # get inputs [B, C, F, T]
    X = torch.randn([2, 2, 256, 401])
    # print network
    summary(model, input_size=tuple(X.shape))
    # forward
    Y_hat = model(X)

    print(f"Test DSConv2d Module End...")
