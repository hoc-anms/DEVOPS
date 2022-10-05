"""
system {
    scripts {
        op {
            file example_op_script.py;
        }
        language python;
    }
}
"""
import argparse
from jnpr.junos import Device
from lxml import etree

# Junos uses this dictionary to generate context sensitive help
arguments = {"interface": "e.g. ge-0/0/0", "family": "e.g. inet / inet6 etc"}


def main():
    parser = argparse.ArgumentParser(description="Show an interface with it's address family")
    # We use the argument dictionary to populate argparse with arguments
    for parameter, description in arguments.iteritems():
        parser.add_argument(('-' + parameter), required=True, help=description)
    args = parser.parse_args()
    # Instantiate a device object, as we are local we don't need any authentication parameters
    dev = Device()
    dev.open()
    # Execute an RPC
    result = dev.rpc.get_interface_information(interface_name=args.interface, terse=True, normalize=True)
    # If you want to see the full xml of the result use: print(etree.tostring(result))
    print("{} status: {}".format(args.interface, result.find('.//oper-status').text))

    for elem in result.xpath("//address-family [normalize-space(address-family-name)=$proto]", proto=args.family):
        if elem.find("interface-address/ifa-local") is not None:
            print("{} family address: {}".format(args.family, elem.find("interface-address/ifa-local").text))
    dev.close()


if __name__ == '__main__':
    main()
