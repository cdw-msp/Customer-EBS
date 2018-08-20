# script that lists all the unencrypted volumes in a region which are in available status and encrypts them
import boto3
ec2 = boto3.resource('ec2', region_name='us-east-1')
def available_volumes():
    existing_volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])
    if existing_volumes:
        for volume in existing_volumes:
            if not volume.encrypted:
                print("Volume with ["+volume.volume_id+"] is in available status and is not encrypted")
                #create_encrypted_volume(volume)
    else:
        print ("No volumes are in  available status")
def create_encrypted_volume(volume):
    print "enter the ARN of your KMSKEYID"
    Kmskey = raw_input() 	
    snapshot = ec2.Snapshot('id')
    created_snapshot = ec2.create_snapshot(
	Description='uday-test-snapshot',
	VolumeId=volume.volume_id,
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
	    KmsKeyId=Kmskey,
	    SourceRegion='us-east-1',
	    SourceSnapshotId=created_snapshot.snapshot_id,
	    )
    print copy_snapshot
    copied_snapshot = ec2.Snapshot(copy_snapshot['SnapshotId'])
    copied_snapshot.wait_until_completed()
	# volume creation from the encrypted copy which is created above
    response = ec2.create_volume(
	    AvailabilityZone=volume.availability_zone,
	    Size=volume.size,
	    VolumeType=volume.volume_type,
		SnapshotId = copy_snapshot['SnapshotId'],
	    TagSpecifications=[
	        {
	            'ResourceType': 'volume',
	            'Tags': volume.tags
	        },
	    ]
	)
    print response	
available_volumes()
