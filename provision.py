import boto
import boto.vpc
import sys

def provision_boto(image_type, student_ids, init_ref, token):
   """ Provisions against MPI VPC on Amazon AWS. Need to place important cloud information into properties or global map """
   #from boto.vpc import VPCConnection
   #
   #mpi_conn = VPCConnection(region=region).get_all_vpcs()

   # image_id = ... ... mpi_conn.get_all_snapshots
   # Cloud Base - no working state, just cloud/node
   # image_id='ami-48c94378'
   # Testing Image - packages, etc as salt-call is broken
   if image_type == "STUDENT":
      image_id='ami-d245d1e2'
   else:
      raise Exception("Cannot provision image type "+image_type)

   mpi_conn = boto.vpc.connect_to_region('us-west-2')

   for cloud in mpi_conn.get_all_vpcs():
      if cloud.id == 'vpc-7af5cb13':
         break

   # Problem here, handle it
   if cloud == None or cloud.id != 'vpc-7af5cb13':
      sys.exit()

   for sn in mpi_conn.get_all_subnets():
      if sn.id == 'subnet-55f5cb3c':
         break

   if sn == None or sn.id != 'subnet-55f5cb3c':
      sys.exit()

   # user_data may be checkout script to start instance, or else salt-master will call minion.
   # Due to serial nature of this, salt-call on minion is sufficient
   # Somewhere I read about using either cloud_init or salt to have multiple instances choose thier own identity
   # either with additional_info or something.  They used an array and they chose metadata via index.  TODO recover

   s_groups = ['sg-763e201a']
   num_students = len(student_ids)

   mpi_conn.run_instances(image_id, min_count=1, max_count=num_students, key_name='neurogenesis', instance_type='t1.micro', subnet_id=sn.id, disable_api_termination=False, instance_initiated_shutdown_behavior=None, private_ip_address=None, client_token=token, security_group_ids=s_groups, additional_info=None, network_interfaces=None)

