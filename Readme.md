# Example for testing SSM Ansible with Localstack and an HTTPS Proxy

## Introduction

## Disclaimer

This example is just a example how you can combine a http proxy with local stack for testing ansible. It is definitely a blueprint for doing secure releases or proper unit testing.

## Implementation

### Http Proxy

* Based on mitmproxy
* Write routing files that forwards *.amazonaws.com to localstack
* Write specific S3 to Localstack logic (e.g., (test-bucket.s3.us-west-1.amazonaws.com --> localstack:4566/test-bucket)

### EC2 Simulation (EC2 Sim)

1. Set HTTPS proxy to your https proxy instance (`docker-compose.yml`)
1. AWS CLI (`Certificate Validation`)
    1. Copy mitmproxy root cert to `/usr/local/share/ca-certificates`
    1. `update-ca-certificates`
2. AWS API with boto3 (`Certificate Validation`)
    1. install with `pip` `certifi`
    1. Make the root certificate available for `certifi`

