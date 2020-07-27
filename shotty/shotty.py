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
#Commands can be attached to other commands of type Group list,stop,start.
@click.group()
def instances():
    """Commands for instances"""
#command for 'List'.
@instances.command('list')
# arguments are passed as parameter declarations to Option:'Project' is passed.
@click.option('--project',default=None,
help="Only Instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"
#project is passed to filter out and get list of instance
    instances = filter_instances(project)
#iterate for getting instance collection sperated
#eg:id,instancetype,state,state,dns,ProjectName
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
    instances()
