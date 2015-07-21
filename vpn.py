#!/usr/bin/python

import fnmatch
import os
import os.path
import argparse

__author__ = 'artemz'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class VpnConnection(object):
    """
    Bare class for vpn connections

    Attributes:
    name
    """

    def __init__(self, name):
        self.name = name

    def enable(self):
        return

    def disable(self):
        return

    def printit(self, accept_all=True):
        print(self.name)


class EnabledVpnConnection(VpnConnection):
    """
    A class for enabled VPN connections
    """

    def enable(self):
        raise "This VPN connection is already enabled"

    def disable(self):
        return

    def printit(self, accept_all=True):
        print(bcolors.OKGREEN + self.name + bcolors.ENDC)


class DisabledVpnConnection(VpnConnection):
    """
    A class for disabled VPN connections
    """

    def disable(self):
        raise "This VPN connection is already disabled"
    def enable(self):
        return
    def printit(self, accept_all=True):
        if accept_all:
            print bcolors.FAIL + self.name + bcolors.ENDC


CONNECTIONS = set()

# Looking up for VPN configurations
for root, dirs, files in os.walk('/etc/openvpn'):
    for f in files:
        if fnmatch.fnmatch(f, '*.conf'):
            CONNECTIONS.add(EnabledVpnConnection(os.path.splitext(f)[0]))
        elif fnmatch.fnmatch(f, '*.conf.off'):
            CONNECTIONS.add(DisabledVpnConnection(f.split(".")[0]))


def list_vpn_connections(args):
    for connection in CONNECTIONS:
        connection.printit(accept_all=args.all)
    return


def enable_vpn_connection(args):
    os.rename("/etc/openvpn/" + args.vpn_connection_name + ".conf.off",
              "/etc/openvpn/" + args.vpn_connection_name + ".conf")
    return


def disable_vpn_connection(args):
    os.rename("/etc/openvpn/" + args.vpn_connection_name + ".conf",
              "/etc/openvpn/" + args.vpn_connection_name + ".conf.off")
    return

argparser = argparse.ArgumentParser(description="Command line utility for managing OpenVPN connections")

action_subparsers = argparser.add_subparsers(help="Action to perform on a VPN connection", dest="command")
list_subparser = action_subparsers.add_parser("list")
list_subparser.add_argument('-a', '--all', action='store_true', default=False)
list_subparser.set_defaults(func=list_vpn_connections)

enable_subparser = action_subparsers.add_parser("enable")
enable_subparser.add_argument("vpn_connection_name")
enable_subparser.set_defaults(func=enable_vpn_connection)

disable_subparser = action_subparsers.add_parser("disable")
disable_subparser.add_argument("vpn_connection_name")
disable_subparser.set_defaults(func=disable_vpn_connection)

args = argparser.parse_args()
args.func(args)
# argparser.print_usage()

