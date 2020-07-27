#imorting necessary Packages
import boto3
import click
#connecting to Session
session = boto3.Session(profile_name ='shotty')
ec2 = session.resource('ec2')
#function filters the project tag and store as list which then can be iterated
def filter_instances(project):
    instances =[]
    if project :
        filters =[{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances
#Main Command group for snapshot,volumes,instances.
@click.group()
def cli():
    """Shotty Manages snapshots"""
#Command Group for Sanpshot to list .
@cli.group('snapshots')
def snapshots():
    """Commands for Snapshots"""
@snapshots.command('list')
# arguments are passed as parameter declarations to Option:'Project' is passed.
@click.option('--project',default=None,
help="Only snapshot for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 Snapshot"
    #project is passed to filter out and get list of instance
    instances = filter_instances(project)
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
    return
#Command Group for volumes to list.
@cli.group('volumes')
def volumes() :
    """Commands for Volumes"""
#command for 'List'.
@volumes.command('list')
# arguments are passed as parameter declarations to Option:'Project' is passed.
@click.option('--project',default=None,
help="Only Volume for project (tag Project:<name>)")
def list_volume(project):
    "List EC2 Volume"
    #project is passed to filter out and get list of instance
    instances = filter_instances(project)
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
# arguments are passed as parameter declarations to Option:'Project' is passed.
@click.option('--project',default=None,
help="Only Instances for project (tag Project:<name>)")
def create_snapshot(project):
    "Create snapshots for EC2 instances"
    instances = filter_instances(project)
    # for each instance,volume,create snapshot
    for i in instances:
        print("Stopping  {0}",format(i.id))
        i.stop()
        i.wait_until_stopped()
        for v in i.volumes.all():
            print("Creating snapshots of{0}".format(v.id))
            v.create_snapshot(Description="Created by SnapshotAlyzer 30000")
        print("Starting  {0}",format(i.id))
        i.start()
        i.wait_until_running()
    print("Done")
    return
#command for 'List.
@instances.command('list')
# arguments are passed as parameter declarations to Option:'Project' is passed.
@click.option('--project',default=None,
help="Only Instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"
    #project is passed to filter out and get list of instance
    instances = filter_instances(project)
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
# arguments are passed as parameter declarations to Option:'Project' is passed.
@click.option('--project',default=None,
   help='Only Instances for project')
#project is passed to filter out and get list of instance
def stop_instances(project):
    "Stop EC2 instances"
    instances =filter_instances(project)
    # for each instance start function is invoked
    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
    return
#command for 'Start'.
@instances.command('start')
# arguments are passed as parameter declarations to Option:'Project' is passed.
@click.option('--project',default=None,
   help='Only Instances for project')
#project is passed to filter out and get list of instance
def start_instances(project):
    "start EC2 instances"
    instances =filter_instances(project)
    # for each instance stop function is invoked
    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()
    return
#invoke the group command
if __name__ == '__main__':
    cli()
