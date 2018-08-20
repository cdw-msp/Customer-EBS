# script that creates a encrypted S3 bucket or if the bucket already exits loops over the objects and encrypts the objects/encrypts the bucket
import boto3
import botocore
s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')
print "enter the s3 bucket name to  create/encrypt"
bucket_name = raw_input()
def check_bucket_exists(bucket):
    return s3_resource.Bucket(bucket) in s3_resource.buckets.all()

if not check_bucket_exists(bucket_name):
	response = s3.create_bucket(Bucket=bucket_name)
	print response
	print "bucket successfully created"
else:
	print "bucket already exists"
	bucket = s3_resource.Bucket(bucket_name)
	for obj in bucket.objects.all():
		key = s3_resource.Object(bucket.name, obj.key)
		print key.server_side_encryption
		print obj.key
		if not key.server_side_encryption:
			response = s3.copy_object(
						Bucket=bucket_name,
						CopySource=bucket_name+'/'+obj.key,
						Key=obj.key,
						ServerSideEncryption='aws:kms',
						SSEKMSKeyId='arn:aws:kms:us-east-1:706839808421:key/ee5956f2-8e2c-4a9b-9876-2eccd219553f'
					)
			print "object successfully encrypted"

response = s3.put_bucket_encryption(Bucket=bucket_name, ServerSideEncryptionConfiguration={
		'Rules': [
		{
		'ApplyServerSideEncryptionByDefault': {
		'SSEAlgorithm': 'aws:kms',
		'KMSMasterKeyID': 'arn:aws:kms:us-east-1:706839808421:key/ee5956f2-8e2c-4a9b-9876-2eccd219553f'
		}
		},
		]
	}
)
print response
print "bucket successfully encrypted"