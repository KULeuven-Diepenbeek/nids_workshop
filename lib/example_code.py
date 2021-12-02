from dataset import NIDSDataset
from nn_model import get_nn_model

import numpy as np
import torch

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


def bytes_as_hexstring(bytes_array):
    """
    Convert a provided array of bytes into a string of hexadecimal characters.
    """

    return "".join(["{:02X}".format(b) for b in bytes_array])


def get_flow_id(packet):

    mac_dst = packet[0:6]
    mac_src = packet[6:12]
    ethertype = packet[12:14]
    # print(ethertype, bytes_to_int(ethertype))

    tot_len = packet[16:18]
    # print(tot_len, bytes_to_int(tot_len))

    id = packet[18:20]
    _ = packet[20:22]
    ttl = packet[22:23]
    protocol = packet[23:24]
    hcks = packet[24:26]
    ip_src_addr = packet[26:30]
    ip_dst_addr = packet[30:34]

    ip_src_addr_str = '{}.{}.{}.{}'.format(ip_src_addr[0], ip_src_addr[1], ip_src_addr[2], ip_src_addr[3])
    ip_dst_addr_str = '{}.{}.{}.{}'.format(ip_dst_addr[0], ip_dst_addr[1], ip_dst_addr[2], ip_dst_addr[3])

    src_port = packet[34:36]
    dst_port = packet[36:38]

    return ip_src_addr_str, ip_dst_addr_str, str(bytes_to_int(src_port)), str(bytes_to_int(dst_port)), str(protocol[0])

def test_model():
    model = get_nn_model()

    dset = NIDSDataset(packets_file='../data/packets-medium.npy', labels_file='../data/labels-medium.npy')

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

    features_storage = {}

    for packet in dset:
        counter = 0
        protocol = ""
        src_addr = ""
        dst_addr = ""
        src_port = ""
        dst_port = ""
        packet_header = np.zeros(64)

        for word in packet:

            if counter == 22:
                protocol = str(bytes_to_int(word[-2:]))
            elif counter == 26:
                src_addr = "{}.{}.{}.{}".format(word[0], word[1], word[2], word[3])
            elif counter == 30:
                dst_addr = "{}.{}.{}.{}".format(word[0], word[1], word[2], word[3])
            elif counter == 34:
                src_port = str(bytes_to_int(word[0:2]))
                dst_port = str(bytes_to_int(word[2:4]))
            try:
                packet_header[counter:counter + 4] = word[:]
            except ValueError:
                continue
            counter += 4
            if counter == 64:
                break

        new_fid = "{}|{}-{}-{}-{}-{}".format(packet.get_label(), src_addr, dst_addr, src_port, dst_port, protocol)

        if new_fid in features_storage.keys():
            features_storage[new_fid].append(packet_header)
        else:
            features_storage[new_fid] = [packet_header]

    # Now extract samples from the dictionary
    for flow_id, features in features_storage.items():
        n_samples = len(features)
        label = flow_id.split('|')[0]

        for i in range(0, n_samples, 5):

            input_sample = np.zeros((5, 64))
            if n_samples - i < 5:
                input_sample[:n_samples - i] = features[i:]
            else:
                input_sample[:] = features[i:i+5]

            # input_sample = input_sample.reshape(1, -1)

            input_tensor = torch.from_numpy(input_sample)
            input_tensor = input_tensor.view(1, 1, 320)

            output_tensor = model(input_tensor.float())
            _, predicted = torch.max(output_tensor, 1)
            print(label_mapping[predicted[0]], label)


def test_flow_id_extraction():
    dset = NIDSDataset(packets_file='packets-medium.npy', labels_file='labels-medium.npy')
    flow_ids = {}
    for packet in dset:
        flow_id = "-".join(get_flow_id(packet.get_data()))

        if not flow_id in flow_ids.keys():
            flow_ids[flow_id] = (packet.get_label(), 1)
        else:
            flow_ids[flow_id] = (packet.get_label(), flow_ids[flow_id][1] + 1)

    for key, item in flow_ids.items():
        print("{}: {}".format(key, item))


def list_protocols():
    dset = NIDSDataset(packets_file='../data/dataset_packets_v1.npy', labels_file='../data/dataset_labels_v1.npy')

    protocols = {}

    for packet in dset:
        counter = 0
        ethertype = ""

        for word in packet:
            if counter == 12:
                ethertype = str(bytes_to_int(word[:2]))

            print(word)
            if ethertype == "2048":
                if counter == 20:
                    protocol = str(bytes_to_int(word[3:]))
                    print("Protocol: ", protocol)
                    final_protocol = ethertype + "-" + protocol
                    if final_protocol in protocols.keys():
                        protocols[final_protocol] += 1
                    else:
                        protocols[final_protocol] = 1
                    break
            elif ethertype != "":
                final_protocol = ethertype
                if final_protocol in protocols.keys():
                    protocols[final_protocol] += 1
                else:
                    protocols[final_protocol] = 1
                break
            counter += 4
            if counter == 64:
                break
    print(protocols)


if __name__ == '__main__':
    #test_model()
    list_protocols()
