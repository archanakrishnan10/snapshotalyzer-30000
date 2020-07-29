# snapshotalyzer-30000
--24/07/2020
A demo project to manage AWS EC2 instance

## About
This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuration

shotty uses the Configuration file created by the AWS Cli. eg

'aws configure -- profile shotty'

## Running
'pipenv run python shotty/shotty.py <command> <--project=PROJECT>'
*command* is a list,start,stop or help
*project* is optional

eg: pipenv run  python shotty/shotty.py start --project='xxxxx'
    pipenv run  python shotty/shotty.py stop --project='xxxxx'
    pipenv run  python shotty/shotty.py list --project='xxxxx'
    pipenv run  python shotty/shotty.py --help

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
   --to list all snapshot
  eg: pipenv run  python shotty/shotty.py snapshots list --all
