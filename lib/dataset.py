import numpy as np


class Packet:

    def __init__(self, bytes_array, label):
        self.__packet = bytes_array
        self.__label = label
        self.__idx = 0

        self.__len = bytes_array.shape[0]
        self.__n_bytes = 14 + self.__bytes_to_int(self.__packet[16:18])
        self.__len_limit = min(self.__len, self.__n_bytes)

    @staticmethod
    def __bytes_to_int(bytes_array):
        n_bytes = len(bytes_array)

        value = 0

        for i in range(n_bytes):
            value += (pow(256, n_bytes - i - 1) * bytes_array[i])

        return value

    def get_label(self):
        """
        Get the label that was assigned to this packet
        :return: The packet's label
        :rtype: ``str``
        """
        return self.__label

    def __str__(self):
        return "{} packet".format(self.__label)

    def __iter__(self):
        self.__idx = 0
        return self

    def __len__(self):
        return self.__len_limit

    def __next__(self):
        if self.__idx >= self.__len_limit:
            raise StopIteration
        elif (self.__idx + 4) >= self.__len_limit:
            word = self.__packet[self.__idx:self.__len_limit]
        else:
            word = self.__packet[self.__idx:self.__idx + 4]
        self.__idx += 4

        return word


class NIDSDataset:
    """
    The nids dataset class provides an interface between the dataset numpy data files and custom code.
    """

    # Default file names for dataset files.
    default_packets_file = "packets.npy"
    defaul_labels_file = "labels.npy"

    # Labels corresponding with the values in the 'labels.npy' file.
    label_mapping = {
        "BENIGN": 0,
        "DDoS": 1,
        "PortScan": 2,
        "Bot": 3,
    }

    def __init__(self, packets_file=None, labels_file=None):

        if packets_file is None:
            self.packets_file = self.default_packets_file
        else:
            self.packets_file = packets_file

        if labels_file is None:
            self.labels_file = self.defaul_labels_file
        else:
            self.labels_file = labels_file

        self.__packets = np.load(self.packets_file)
        self.__labels = np.load(self.labels_file)

        self.__n_packets = self.__packets.shape[0]
        self.__n_bytes = self.__packets.shape[1]

        self.__current_packet_idx = 0

    def __get_label(self, label_idx):

        for label, idx in self.label_mapping.items():
            if idx == label_idx:
                return label
        return None

    def __len__(self):
        return self.__n_packets

    def __getitem__(self, item):
        return Packet(self.__packets[item][:], self.__get_label(int(self.__labels[item])))

    def __iter__(self):
        self.__current_packet_idx = -1

        return self

    def __next__(self):

        self.__current_packet_idx += 1

        if self.__current_packet_idx == self.__n_packets:
            raise StopIteration

        return self[self.__current_packet_idx]


#dset = NIDSDataset()

#print(len(dset))
#print(dset.labels)
#print(dset.packets.shape)
#print(dset.packets[9], dset.labels[9])

#print(dset.get_flow_id(0))
#print("".join(["{:02X}".format(dset[0][0][i]) for i in range(100)]))

#for packet in iter(dset):
#    print(packet)
#    for word in packet:
#        print(word)

#for i in range(len(dset)):
#    print(dset.get_flow_id(i))
