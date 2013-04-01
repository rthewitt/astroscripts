import boto
import boto.vpc
import time
import sys
import salt, salt.key, salt.runner, salt.client
from jinja2 import Environment, FileSystemLoader

def provision_boto(image_type, student_ids, init_ref, token):
   """ Provisions against MPI VPC on Amazon AWS. Need to place important cloud information into properties or global map """
   # image_id = ... ... mpi_conn.get_all_snapshots
   if image_type == "STUDENT":
      image_id='ami-d245d1e2'
   else:
      # Cloud Base image_id='ami-48c94378'
      raise Exception("Cannot provision image type "+image_type)

   mpi_conn = boto.vpc.connect_to_region('us-west-2')

   for cloud in mpi_conn.get_all_vpcs():
      if cloud.id == 'vpc-7af5cb13':
         break

   # Problem here, handle it
   if cloud is None or cloud.id != 'vpc-7af5cb13':
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

   reservation = mpi_conn.run_instances(image_id, min_count=1, max_count=num_students, key_name='neurogenesis', instance_type='t1.micro', subnet_id=sn.id, disable_api_termination=False, instance_initiated_shutdown_behavior=None, private_ip_address=None, client_token=token, security_group_ids=s_groups, additional_info=None, network_interfaces=None)

   # get instances to create or modify file
   w_res = reservation

   # loop until reservation instances are running
   pending = True
   while pending
      instances = w_res.instances
      pending = False
      for instance in instances:
         if instance.state != 'running':
            if instance.state != 'pending':
               print "unexpected instance state for instance", instance.id, ":", instance.state
            else:
               print "instances pending..."
               pending = True
               break # from for loop
      if pending:
         time.sleep(20)
         old_res = w_res # convieniently does not maintain equality upon refresh
         for rez in mpi_conn.get_all_instances():
            if rez.id == reservation.id:
               w_res = rez
         if old_res == w_res: # should have changed
            raise Exception("reservation object did NOT change between requests")


   # ====== HANDLE SALT ===========
   opts = salt.config.master_config('/etc/salt/master')
   sk = salt.key.Key(opts)
   lc = salt.client.LocalClient(opts)
   rc = salt.runner.RunnerClient(opts)

   # rc.cmd('manage.status',[]) ['up'/'down']
   # sk.list_keys() ['minions' / 'minions_pre' / 'minions_rejected']

   expected = [i.private_dns_name.split('.')[0] for i in instances]
   if not len(expected) == len(student_ids):
      s_data = zip(expected, student_ids)
   else:
      raise Exception("Something went wrong: "+len(student_ids)+" students and "+len(expected)+" minions")

   # jinja template
   t_env = Environment(loader=FileSystemLoader('templates'))
   t_sls = t_env.get_template('student-pillar.sls')
   
   # write to pillar sls, and then call top after accepting minions
   # Note: they may actually top themselves after being accepted
   student_pillar = t_sls.render(minions=s_data)
   print "rendered sls:", student_pillar
   with open("/srv/pillar/student-data.sls", "wb") as ff:
      ff.write(student_pillar)

   for minion in expected:
      if minion not in sk.list_keys()['minions_pre']:
         print "minion not yet detected, sleeping once"
         sleep(30)
         if minion not in sk.list_keys()['minions_pre']:
            raise Exception("minion", minion, "not found")
      # accept these instances via salt-key
      sk.accept_key(minion)

   for minion in expected:
      if minion not in rc.cmd('manage.status',[])['up']:
         raise Exception("Minion not responding:", minion



def test(image_type='STUDENT', student_ids=['test-1','test-2'], init_ref='check-0', token=None):
   if token is None:
      raise Exception('must provide token')
   return provision_boto(image_type, student_ids, init_ref, 'test-token-'+token)

def main():
   return test(token='test-token-'+sys.argv[1])


if __name__ == '__main__':
   main()
