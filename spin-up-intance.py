from boto import boto
import sys
#from boto.vpc import VPCConnection
#
#for region in boto.ec2.regions():
#   if region.name == 'us-west-2':
#      break
#
## Problem here, handle it
#if region == None:
#   sys.exit()
#
#mpi_conn = VPCConnection(region=region).get_all_vpcs()

mpi_conn = boto.vpc.connect_to_region('us-west-2')

for vpc in mpi_conn:
   if vpc.id == 'vpc-7af5cb13':
      break

# Problem here, handle it
if vpc == None or vpc.id != 'vpc-7af5cb13':
   sys.exit()

for sn in mpi_conn.get_all_subnets:
   if sn.id == 'subnet-55f5cb3c':
      break

if sn == None or sn.id != 'subnet-55f5cb3c':
   sys.exit()

# image_id = ... ... mpi_conn.get_all_snapshots
# num_students (argument or inferred from argument)
# user_data may be checkout script to start instance, or else salt-master will call minion.
# Due to serial nature of this, salt-call on minion is sufficient
# Somewhere I read about using either cloud_init or salt to have multiple instances choose thier own identity
# either with adidtional_info or something.  They used an array and they chose metadata via index.  TODO recover

image_id='ami-48c94378'
# create a client token for request, or each machine (idempotency)
client_token='slSCXikdksOOLsp'

mpi_conn.run_instances(image_id, min_count=1, max_count=num_students, key_name='neurogenesis', security_groups=['Student VM'], instance_type='t1.micro', subnet_id=sn.id, disable_api_termination=False, instance_initiated_shutdown_behavior=None, private_ip_address=None, client_token=None, security_group_ids=None, additional_info=None, network_interfaces=None)

