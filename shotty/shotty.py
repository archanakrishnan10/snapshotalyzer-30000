#imorting necessary Packages
import boto3
import botocore
import click
#connecting to Session
session = boto3.Session(profile_name ='shotty')
ec2 = session.resource('ec2')
#function filters the project tag and returns as list which then can be iterated
def filter_instances(project,force_all):
    instances =[]
    if project :
        filters =[{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    elif force_all :
        instances = ec2.instances.all()
    else:
        print("Warning:Project is not Set, Please set the project or do --force")

    return instances
#function returns pending snapshots.
 #def has_pending_snapshot(volume):
    #snapshots = list(volume.snapshots.all())
    #return snapshots and snapshots[0].state =='pending'

#Main Command group for snapshot,volumes,instances.
@click.group()
def cli():
    """Shotty Manages snapshots"""

#Command Group for Sanpshot to list .
@cli.group('snapshots')
def snapshots():
    """Commands for Snapshots"""
@snapshots.command('list')
# arguments are passed as parameter options: --project 'xxxxx'
@click.option('--project',default=None,
help="Only snapshot for project (tag Project:<name>)")
# arguments are passed as parameter options: --all
@click.option('--all','list_all',default = False,is_flag = True,
help="List All snapshots of each Volume on request for --all")
@click.option('--force','force_all',default = True,
      help="List All snapshots")
def list_snapshots(project,list_all,force_all):
    "List EC2 Snapshot"
    #project is passed to filter out and get list of instance
    instances = filter_instances(project,force_all)
    #iterate for getting instance,volume and its snapshot details together
    #eg:id,volume id,instance id,state,progress,start time
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                s.id,
                v.id,
                i.id,
                s.state,
                s.progress,
                s.start_time.strftime("%c")
                )))
                #to get the most recent successfull snapshot and break the loop
                if s.state == 'completed' and not list_all: break
    return

#Command Group for volumes to list.
@cli.group('volumes')
def volumes() :
    """Commands for Volumes"""
#command for 'List'.
@volumes.command('list')
# arguments are passed as parameter options: --project 'xxxxx' .
@click.option('--project',default=None,
help="Only Volume for project (tag Project:<name>)")
@click.option('--force','force_all',default = True,
      help="List All Volumes")
def list_volume(project,force_all):
    "List EC2 Volume"
    #project is passed to filter out and get list of instance
    instances = filter_instances(project,force_all)
    #iterate for getting instance and volume details together for consistency
    #eg:id,instance id,state,size,encrypted(boolean)
    for i in  instances :
        for v in i.volumes.all():
            print(",".join((v.id,
            i.id,
            v.state,
            str(v.size)+'GiB',
            v.encrypted and "encrypted" or "Not encrypted"
            )))
    return
#Commands Group for instances to create snapshot and list,stop,startinstances.
@cli.group('instances')
def instances():
    """Commands for instances"""
#command for 'creating snapshots.
@instances.command('snapshots',help="Create snapshots of all volumes")
# arguments are passed as parameter options: --project 'xxxxx'
@click.option('--project',default=None,
help="Only Instances for project (tag Project:<name>)")
@click.option('--force','force_all',default = False,is_flag = True,
      help="Create snapshots for all")
def create_snapshot(project,force_all):
    "Create snapshots for EC2 instances"
    instances = filter_instances(project,force_all)
    # for each instance,volume,create snapshot
    for i in instances:
        print("Stopping  {0}",format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            #if has_pending_snapshot(v):
                #print("Skipping {0},snapshot already in progress".format(v.id))
                #continue
            #print("Creating snapshots of{0}".format(v.id))
            try :
                print("Creating snapshots of{0}".format(v.id))
                v.create_snapshot(Description="Created by SnapshotAlyzer 30000")
            except botocore.exceptions.ClientError as e :
                print("Snapshot already in progress {0}. ",format(i.id)+ str(e))
                continue
        print("Starting  {0}".format(i.id))
        i.start()
        i.wait_until_running()
    print("Done")
    return
#command for 'List.
@instances.command('list')
# arguments are passed as parameter options: --project 'xxxxx'
@click.option('--project',default=None,
help="Only Instances for project (tag Project:<name>)")
@click.option('--force','force_all',default = True,
      help="List All instances")
def list_instances(project,force_all):
    "List EC2 instances"
    #project is passed to filter out and get list of instance
    instances = filter_instances(project,force_all)
    #iterate for getting instance collection sperated
    #eg:id,instancetype,placement,state,dns,ProjectName
    for i in instances :
        # convert tag(see boto3 docs) as dictionary and iterate then print
        tags={t['Key']: t['Value'] for t in i.tags or []}
        print(','.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project','<no project>'))))
    return
#command for 'Stop'.
@instances.command('stop')
# arguments are passed as parameter options: --project 'xxxxx'
@click.option('--project',default=None,
   help='Only Instances for project')
@click.option('--force','force_all',default = False,is_flag = True,
   help="Force stop All instances")
#project is passed to filter out and get list of instance
def stop_instances(project,force_all):
    "Stop EC2 instances"
    instances =filter_instances(project,force_all)
    # for each instance stop function is invoked
    for i in instances:
        print("Stopping {0}...".format(i.id))
        #exception handling for overlaping start/stop
        try:
           i.stop()
        except botocore.exceptions.ClientError as e :
           print("Could not stop {0}. ",format(i.id)+ str(e))
           continue
    return
#command for 'Start'.
@instances.command('start')
# arguments are passed as parameter options: --project 'xxxxx'
@click.option('--project',default=None,
   help='Only Instances for project')
@click.option('--force','force_all',default = False,is_flag = True,
      help="Force start All instances")
#project is passed to filter out and get list of instance
def start_instances(project,force_all):
    "start EC2 instances"
    instances =filter_instances(project,force_all)
    # for each instance stop function is invoked
    for i in instances:
        print("Starting {0}...".format(i.id))
        #exception handling for overlaping start/stop
        try:
            i.start()
        except botocore.exceptions.ClientError as e :
            print("Could not start {0}. ",format(i.id)+ str(e))
            continue
    return

#command for 'Reboot'.
@instances.command('reboot')
# arguments are passed as parameter options: --project 'xxxxx'
@click.option('--project',default=None,
   help='Only Instances for project')
@click.option('--force','force_all',default = False,is_flag = True,
      help="Force reboot All instances")
#project is passed to filter out and get list of instance
def reboot_instances(project,force_all):
    "reboot EC2 instances"
    instances =filter_instances(project,force_all)
    # for each instance reboot function is invoked
    for i in instances:
        print("Rebooting {0}...".format(i.id))
        #exception handling for overlaping start/stop for reboot
        try:
            i.reboot()
        except botocore.exceptions.ClientError as e :
            print("Could not reboot instance {0}. ",format(i.id)+ str(e))
            continue
    return
#invoke the main group command
if __name__ == '__main__' :
#if 1==1 :
    cli()
