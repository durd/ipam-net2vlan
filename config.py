import argparse

class Config:
  def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument('parentsubet', help='Master subnet, can not be a subnet that has VLAN assigned and whos child subnets don\'t have VLANs assigned')
    parser.add_argument('-i', '--ipamurl', help='IPAMs URL: http://<hostname or IP> | https://<hostname or IP>')
    parser.add_argument('-ip', '--ipampassword', help='IPAM password')
    parser.add_argument('-iu', '--ipamusername', help='IPAM username')
    parser.add_argument('-ia', '--ipamapp', help='IPAM API app')
    self.config = parser.parse_args()

  def get_parentsubnet(self):
    return self.config.parentsubnet

  def get_ipam_url(self):
    return self.config.ipamurl

  def get_ipam_app(self):
    return self.config.ipamapp

  def get_ipam_username(self):
    return self.config.ipamusername

  def get_ipam_password(self):
    if self.config.ipampassword is not None:
        return self.config.ipampassword
    else:
        return ''
