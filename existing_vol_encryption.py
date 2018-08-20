# script that creates a snapshot from exsiting unencrypted volume, creates a encrypted copy of the snapshot and creates a encypted volume from the copy
import boto3
ec2 = boto3.resource('ec2')
#snapshot creation from the existing unencrypted volume
snapshot = ec2.Snapshot('id')
created_snapshot = ec2.create_snapshot(
    Description='uday-test-snapshot',
    VolumeId='vol-066d9db72f547bbdf',
    TagSpecifications=[
        {
            'ResourceType': 'snapshot',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'test-snapshot'
                },
            ]
        },
    ]
    
)
print created_snapshot
created_snapshot.wait_until_completed()
#creating the encrypted copy of the snapshot which is created above
copy_snapshot = snapshot.copy(Description='uday-test-copy',
    Encrypted=True,
    KmsKeyId='arn:aws:kms:us-east-1:706839808421:key/ee5956f2-8e2c-4a9b-9876-2eccd219553f',
    SourceRegion='us-east-1',
    SourceSnapshotId=created_snapshot.snapshot_id,
    )
print copy_snapshot
copied_snapshot = ec2.Snapshot(copy_snapshot['SnapshotId'])
copied_snapshot.wait_until_completed()
# volume creation from the encrypted copy which is created above
response = ec2.create_volume(
    AvailabilityZone='us-east-1a',
    Size=10,
    VolumeType='gp2',
	SnapshotId = copy_snapshot['SnapshotId'],
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'test-volume'
                },
            ]
        },
    ]
)
print response