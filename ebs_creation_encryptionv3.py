# script that creates a new encrypted EBS volumes where the parameters are passed thorugh the keyboard using the raw_input() function
import boto3
ec2 = boto3.resource('ec2')
volume = ec2.Volume('id')
print "enetr the availabilty zone that you want to create your volume. ex:us-east-1a "
availabilty_zone = raw_input()
print "enter the ARN of your KMSKEYID"
Kmskey = raw_input()
print "enter the size of your volume in GiBs. This should be integer"
size_vol = raw_input()
print "enter the volume type you want. ex:gp2"
volume_type = raw_input()
print "enter the name for your volume"
tag_name = raw_input()
response = ec2.create_volume(
    AvailabilityZone=availabilty_zone,
	Encrypted=True,
    KmsKeyId=Kmskey,
    Size=int(size_vol),
    VolumeType=volume_type,
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': tag_name

                },
            ]
        },
    ]
)
print response