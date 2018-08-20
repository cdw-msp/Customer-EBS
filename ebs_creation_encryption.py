# script that creates a new encrypted EBS volume

import boto3
ec2 = boto3.resource('ec2')
volume = ec2.Volume('id')
response = ec2.create_volume(
    AvailabilityZone='us-east-1a',
    Encrypted=True,
    KmsKeyId='xxxxxxxxxxxxxxxxxxx',
    Size=10,
    VolumeType='gp2',
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'uday-test-volume1'
                },
            ]
        },
    ]
)
print response