from dataset import NIDSDataset, bytes_to_int


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


if __name__ == '__main__':
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