# AWS EC2 instance example test

This example test demonstrates the capabilities of the Robotframework Terraform Library.
The test
- creates an AWS EC2 instance in your AWS account
- connects to the instance via SSH
- extracts the hostname
- verifies the hostname against the private DNS of the instances

## Requirements
The following pip packages need to be installed
- Robotframework
- Robotframework-SSHLibrary
- Robotframework-TerraformLibrary

AWS access credentials are exposed to the environment.
The following environment variables are set as inputs to the terraform script.
- `TF_VAR_aws_ssh_key`containing the name of an SSH key pair stored in the AWS account.
- `TF_VAR_subnet` containing a subnet ID of the VPC where the EC2 instance should be created in.
- `TF_VAR_security_group` containing the ID of a security group allowing SSH traffic on port 22.

The private key file for the SSH access to the EC2 instance. (Filename `private_key.pem`)
