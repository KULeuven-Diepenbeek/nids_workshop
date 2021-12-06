import torch
import torch.nn as nn


label_mapping = [
        "BENIGN",
        "Bot",
        "PortScan",
        "DDoS",
        "Web Attack",
        "Infiltration",
        "DoS GoldenEye",
        "DoS Hulk",
        "DoS Slowhttptest",
        "DoS slowloris",
        "Heartbleed",
        "FTP-Patator",
        "SSH-Patator",
    ]


class ExampleCNN1D4x64(nn.Module):
    """
    Class implementing a small 1D CNN for 4x64 input features.
    """
    def __init__(self, num_classes=10):
        super(ExampleCNN1D4x64, self).__init__()

        self.num_class = num_classes

        self.layer1 = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=5, stride=1, dilation=1, padding=2, bias=True),  # -> 256 x 16
            nn.BatchNorm1d(num_features=16, eps=1e-05, momentum=0.95, affine=True),
            nn.ReLU(),
        )

        self.maxpool1 = nn.MaxPool1d(kernel_size=2, stride=2)   # -> 128 x 16

        self.layer2 = nn.Sequential(
            nn.Conv1d(16, 32, kernel_size=5, stride=1, dilation=1, padding=2, bias=True),  # -> 128 x 32
            nn.BatchNorm1d(num_features=32, eps=1e-05, momentum=0.95, affine=True),
            nn.ReLU(),
        )

        self.maxpool2 = nn.MaxPool1d(kernel_size=2, stride=2)   # -> 64 x 32

        self.layer3 = nn.Sequential(
            nn.Conv1d(32, 64, kernel_size=5, stride=1, dilation=1, padding=2, bias=True),  # -> 64 x 64
            nn.BatchNorm1d(num_features=64, eps=1e-05, momentum=0.95, affine=True),
            nn.ReLU(),
        )

        self.maxpool3 = nn.MaxPool1d(kernel_size=4, stride=4)  # -> 16 x 64

        self.layer4 = nn.Sequential(
            nn.Conv1d(64, 96, kernel_size=3, stride=1, dilation=1, padding=1, bias=True),  # -> 16 x 96
            nn.BatchNorm1d(num_features=96, eps=1e-05, momentum=0.95, affine=True),
            nn.ReLU(),
        )

        self.maxpool4 = nn.MaxPool1d(kernel_size=16, stride=1)   # -> 1 x 96

        self.classification = nn.Linear(in_features= 1 * 96, out_features=self.num_class, bias=True)

    def __convolve(self, x):
        x = self.layer1(x)
        x = self.maxpool1(x)
        x = self.layer2(x)
        x = self.maxpool2(x)
        x = self.layer3(x)
        x = self.maxpool3(x)
        x = self.layer4(x)
        x = self.maxpool4(x)

        return x

    def forward(self, x):
        # Process convolution operations
        x = self.__convolve(x)
        # Reshape the features to a 1D vector: n_batches x (input_size / 16 * 256)
        x = x.view(x.shape[0], -1)

        # print(x.shape)

        # Perform classification
        x = self.classification(x)

        return x


class ExampleCNN1D1x64(nn.Module):
    """
    Class implementing a small 1D CNN for 5x64 input features.
    """
    def __init__(self, num_classes=10):
        super(ExampleCNN1D1x64, self).__init__()

        self.num_class = num_classes

        self.layer1 = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=(5,), stride=(1,), dilation=(1,), padding=(2,), bias=True),  # -> 64 x 16
            nn.BatchNorm1d(num_features=16, eps=1e-05, momentum=0.95, affine=True),
            nn.ReLU(),
        )

        self.pool1 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.layer2 = nn.Sequential(
            nn.Conv1d(16, 32, kernel_size=(5,), stride=(1,), dilation=(1,), padding=(2,), bias=True),  # -> 32 x 32
            nn.BatchNorm1d(num_features=32, eps=1e-05, momentum=0.95, affine=True),
            nn.ReLU(),
        )

        self.pool2 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.layer3 = nn.Sequential(
            nn.Conv1d(32, 64, kernel_size=(5,), stride=(1,), dilation=(1,), padding=(2,), bias=True),  # -> 16 x 64
            nn.BatchNorm1d(num_features=64, eps=1e-05, momentum=0.95, affine=True),
            nn.ReLU(),
        )

        self.pool3 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.layer4 = nn.Sequential(
            nn.Conv1d(64, 96, kernel_size=(3,), stride=(1,), dilation=(1,), padding=(1,), bias=True),  # -> 8 x 96
            nn.BatchNorm1d(num_features=96, eps=1e-05, momentum=0.95, affine=True),
            nn.ReLU(),
        )

        self.pool4 = nn.MaxPool1d(kernel_size=2, stride=2)

        self.classification = nn.Linear(in_features=4*96, out_features=self.num_class, bias=True)

    def __convolve(self, x):
        x = self.layer1(x)
        x = self.pool1(x)
        x = self.layer2(x)
        x = self.pool2(x)
        x = self.layer3(x)
        x = self.pool3(x)
        x = self.layer4(x)
        x = self.pool4(x)
        return x

    def forward(self, x):
        # Process convolution operations
        x = self.__convolve(x)
        # Reshape the features to a 1D vector
        x = x.view(x.shape[0], -1)

        # Perform classification
        x = self.classification(x)

        return x
