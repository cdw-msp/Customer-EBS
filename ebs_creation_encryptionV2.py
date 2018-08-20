# script that creates a new encrypted EBS volumes where the parameters are passed as arguments
import boto3
import sys
ec2 = boto3.resource('ec2')
volume = ec2.Volume('id')
arguments = sys.argv[0]
availabilty_zone= sys.argv[1]
kms_keyid = sys.argv[2]
vol_size = sys.argv[3]
vol_type = sys.argv[4]
vol_name = sys.argv[5]
response = ec2.create_volume(
    AvailabilityZone=availabilty_zone,
	Encrypted=True,
    KmsKeyId=kms_keyid,
    Size=int(vol_size),
    VolumeType=vol_type,
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': vol_name

                },
            ]
        },
    ]
)
print response