import phpypam
import json
import urllib3
import getpass
import sys

from config import Config

# silence self-signed certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ipam_search_childsubnets(pi, parentsubnet):
  print('Fetching child subnets unders {}'.format(parentsubnet))
  parent = pi.get_entity('subnets', '/cidr/' + parentsubnet)

  children = pi.get_entity('subnets', parent[0]['id'] + '/slaves/')

  childvlans = []
  for k in children:
    if k['vlanId'] != '0' and 'xxx' not in k['description'].lower():
      childvlans.append(k)

  subnets = []
  for k in childvlans:
    k['vlan-number'] = pi.get_entity('vlan', k['vlanId'])['number']
    print('{} - {}'.format(k['vlanId]', k['description']))
    subnets.append(k)
  return subnets

def main():
  config = Config()
  ipamparams = dict(
    url = config.get_ipam_url(),
    app_id = config.get_ipam_app(),
    username = config.get_ipam_username(),
    password = config.get_ipam_password(),
    ssl_verify = False
  )
  parentsubnet = config.get_parentsubnet()
  try:
    if ipamparams['password'] == '':
      if sys.stdin.isatty():
        ipamparams['password'] = getpass.getpass()
      else:
        print('Attention! Your password will be shown on the screen!')
        ipamparams['password'] = input('Password: ')
  except KeyboardInterrupt:
    exit(1)
  pi = phpypam.api(**ipamparams)
  childsubnets = ipam_search_childsubnets(pi, parentsubnet)
    
  for i in childsubnets:
    new_name = {'name': i['description']}
    vlan_number = i['vlan_number']
    vlanId = i['vlanId']
    vlan = pi.get_entity('vlan', vlanId)
    vlan_name = vlan['name']
    net_description = i['description']
    print('Setting description for VLAN {} ({})'.format(vlan_number, net_description))
    print('Old: {}'.format(vlan_name))
    print('New: {}'.format(net_description))
    pi.update_entity('vlan', i['vlanId'], new_name)

if __name__ == '__main__':
  main()
