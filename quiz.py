#!/usr/bin/env python

from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

message = b'gAAAAABb4fh_YHUxdg-DT_RRvszBNFmSBEht0Njd2yQQzUeWqUxc-Q7pq-oO_c7mVFUnmvL_L03goKtQ5IPYapP9dD8wMUc2QohIl4TqDdRsFA2H0k9w1gyXWlmAg8dhM_C7PVM3qZYD0TPVqnTQEjfjGYuCjqD-5WHFRPGukqdVwsLiVMzaJLGWDtPCSiNPSU1IQbOf2PUE'


def main():
    """main application"""
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == '__main__':
    main()
