import numpy as np


def bytes_to_int(bytes_array):
    """
    Calculate the integer value that is represented by the provided array of bytes.
    Example: Input is [8, 0], which represents the hexadecimal 0x0800 number. This function will then calculate
    8 * 16^2 + 0 * 16^1 = 2048

    :param bytes_array: Array/list of bytes
    :type bytes_array: ``list`` of ``int``
    :return: The integer value represented by the array of bytes.
    :rtype: ``int``
    """
    n_bytes = len(bytes_array)

    value = 0

    for i in range(n_bytes):
        value += (pow(256, n_bytes - i - 1) * bytes_array[i])

    return value


class Packet:

    def __init__(self, bytes_array, label):
        self.__packet = bytes_array
        self.__label = label
        self.__idx = 0

        self.__len = bytes_array.shape[0]
        self.__n_bytes = 14 + bytes_to_int(self.__packet[16:18])

    def get_label(self):
        """
        Get the label that was assigned to this packet
        :return: The packet's label
        :rtype: ``str``
        """
        return self.__label

    def get_data(self):
        """
        Get the actual data of the packet.
        :return: The data of the packet
        :rtype: numpy.ndarray
        """
        return self.__packet

    def packet_as_hexstring(self):
        """
        Get the contents of the packet as a hexidecimal string
        :return: The packet as a hexadecimal string
        :rtype: ``str``
        """
        return "".join(["{:02X}".format(single_byte) for single_byte in self.__packet])

    def __str__(self):
        return "{}, {}B|{}".format(self.__label, self.__n_bytes, self.packet_as_hexstring())

    def __iter__(self):
        self.__idx = 0
        return self

    def __next__(self):
        if self.__idx >= self.__n_bytes:
            raise StopIteration
        elif (self.__idx + 4) >= self.__n_bytes:
            word = self.__packet[self.__idx:self.__n_bytes]
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

        self.current_packet_idx = 0

    def __get_label(self, label_idx):

        for label, idx in self.label_mapping.items():
            if idx == label_idx:
                return label
        return None

    def __len__(self):
        return self.__n_packets

    def __getitem__(self, item):
        return Packet(self.__packets[item][:], self.__get_label(int(self.__labels[item])))

    def get_number_packets(self):
        """
        Get the number of packets in the dataset.

        :return: The number of packets in the dataset.
        """
        return self.__n_packets

    def get_bytes_per_packet(self):
        """
        Get the maximum number of bytes for a packet in the dataset.

        :return: The maximum number of bytes for each packet in the dataset.
        """
        return self.__n_bytes

    def __iter__(self):
        self.current_packet_idx = -1

        return self

    def __next__(self):

        self.current_packet_idx += 1

        if self.current_packet_idx == self.__n_packets:
            raise StopIteration

        return self[self.current_packet_idx]


dset = NIDSDataset()

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