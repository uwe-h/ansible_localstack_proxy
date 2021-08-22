import os
import base64
import hashlib

import unittest
import boto3



class MyTestCase(unittest.TestCase):
    key_id = None

    @classmethod
    def setUpClass(cls):
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket="top-sec-software")
        with open(f'{os.path.dirname(__file__)}/2021-08-18.tar.gz', 'rb') as f:
            print(s3_client.put_object(Bucket="top-sec-software", Key="our_soft/2021-08-18.tar.gz", Body=f))

        kms_client = boto3.client("kms")
        key_resp = kms_client.create_key(
            KeyUsage='SIGN_VERIFY',
            CustomerMasterKeySpec='RSA_4096',
            Origin='AWS_KMS',
        )
        cls.key_id = key_resp['KeyMetadata']['KeyId']
        print(key_resp)
        with open(f'{os.path.dirname(__file__)}/2021-08-18.tar.gz', 'rb') as f:
            #Read the whole file at once
            data = f.read()
            sha = hashlib.sha256()
            sha.update(data)
            shavalue = sha.digest()
        signature_bytes = kms_client.sign(
            KeyId=cls.key_id,
            Message=shavalue,
            MessageType="DIGEST",
            SigningAlgorithm='RSASSA_PSS_SHA_256'
        )['Signature']
        print("Signature Bytes", signature_bytes)
        signature = base64.b64encode(signature_bytes).decode('ascii')
        print(signature)
        dyn_client = boto3.client("dynamodb")
        try:
            dyn_client.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'release',
                        'AttributeType': 'S',
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName': 'release',
                        'KeyType': 'HASH',
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5,
                },
                TableName='top_sec_download_meta',
            )
        except Exception as e:
            print("e")
        response = dyn_client.put_item(
            TableName='top_sec_download_meta',
            Item={
                'release': {
                    'S': '2021-08-18'
                },
                'signature': {
                    'S': signature
                }
            })


    def test_something(self):
        print(f'ansible-playbook -vvv --connection=local --inventory 127.0.0.1, --limit 127.0.0.1 --extra-vars "key_id={self.key_id}" {os.path.dirname(__file__)}/../src/ansible.yml')
        os.system(f'ansible-playbook --connection=local --inventory 127.0.0.1, --limit 127.0.0.1 --extra-vars "key_id={self.key_id}" {os.path.dirname(__file__)}/../src/ansible.yml')
        self.assertEqual(os.path.isfile("/tmp/successful_check.txt") , True)

if __name__ == '__main__':
    unittest.main()
