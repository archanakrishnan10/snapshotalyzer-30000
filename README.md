# snapshotalyzer-30000
--24/07/2020
A demo project to manage AWS EC2 instance

## About
This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuration

shotty uses the Configuration file created by the AWS Cli. eg

'aws configure -- profile shotty'

--27/07/2020
## Running
    'pipenv run python shotty/shotty.py <command> <subcommand> <--project=PROJECT>'
    *command* instances,snapshots,volume or help
    *sub command* list,create,start,stop
    *project* is optional

  eg: pipenv run  python shotty/shotty.py instances list
      pipenv run  python shotty/shotty.py snapshots list
      pipenv run  python shotty/shotty.py instances start --project xxxxx
      pipenv run  python shotty/shotty.py instances stop --project xxxxx
      pipenv run  python shotty/shotty.py instances list --project xxxxx
      --create snapshot command
      pipenv run  python shotty/shotty.py instances snapshots --project xxxxx


--28/07/2020
  Added code to list only recent snapshots for each volume.Else provide all to list all snapshots
   --to list all snapshot for each volumes
  eg: pipenv run  python shotty/shotty.py snapshots list --all


--29/07/2020
Modified code to provide project name /--force to start/stop/snapshot/reboot instances. Else throw warning.(--force will start/stop/create snapshot/reboot All EC2 instances regardless of project)
pipenv run  python shotty/shotty.py instances start --project xxxxx
pipenv run  python shotty/shotty.py instances start --force
pipenv run  python shotty/shotty.py instances snapshots --project xxxxx
pipenv run  python shotty/shotty.py instances snapshots --force
pipenv run  python shotty/shotty.py instances stop --project xxxxx
pipenv run  python shotty/shotty.py instances stop ----force
pipenv run  python shotty/shotty.py instances list --project xxxxx
pipenv run  python shotty/shotty.py instances list --force
Added code to reboot instances:
pipenv run  python shotty/shotty.py instances reboot --project xxxxx
pipenv run  python shotty/shotty.py instances reboot --force

Modified script to accept instance filter to start/stop/snapshot/reboot only given instance id.
Eg:
pipenv run  python shotty/shotty.py instances stop --instance 'i-x0xxx12xxxx678'
