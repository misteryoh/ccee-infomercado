import boto3
from botocore.exceptions import ClientError

class S3Api:

    def __init__(self, profile=None, region_name='sa-east-1'):
        self.profile = profile
        self.region_name = region_name

    def upload_s3_object(self, content, bucket, folder, filename) -> dict:
        """Upload an object to an S3 bucket

        :param content: Content to upload
        :param bucket: S3 bucket name
        :param folder: Folder name
        :param filename: S3 object name
        :return: dict
        """

        # Create a session using the specified configuration file
        if self.profile is None:
            session = boto3.Session()
        else:
            session = boto3.Session(profile_name=self.profile, region_name=self.region_name)

        s3_client = session.client('s3')

        try:
            # Put object into the S3 bucker
            s3_object = s3_client.put_object(
                Bucket=bucket, Key=f"{folder}/{filename}", Body=content)
        except ClientError as err:
            return {
                'status_code' : 400,
                'body' : err
            }
        
        return {
            'status_code' : 200,
            'body' : 'Upload realizado com sucesso'
        }