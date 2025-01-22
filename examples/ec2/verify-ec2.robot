*** Settings ***
Library    SSHLibrary
Library    TerraformLibrary    executable=tofu

*** Test Cases ***
Create, Verify and Destroy EC2 Instance
    Create EC2 Instance via Terraform
    Get EC2 Instance details from Terraform State
    Connect to EC2
    Get Hostname
    Compare private DNS with Hostname
    [Teardown]    Destroy EC2 Instance via Terraform

*** Keywords ***
Create EC2 Instance via Terraform
    ${rc}    ${output}    Terraform Init    examples/ec2
    Log    ${output}
    IF    ${rc} != 0    Fail    Terraform Error:\n${output}
    ${rc}    ${output}    Terraform Apply    examples/ec2
    Log    ${output}
    IF    ${rc} != 0    Fail    Terraform Error:\n${output}

Get EC2 Instance details from Terraform State
    ${output}    Get Terraform State    examples/ec2
    VAR    ${TF_STATE}    ${output}    scope=TEST
    VAR    ${EC2_PUBLIC_DNS}
    ...    ${TF_STATE["values"]["outputs"]["instance_public_dns"]["value"]}
    ...    scope=TEST
    VAR    ${EC2_PRIVATE_DNS}
    ...    ${TF_STATE["values"]["outputs"]["instance_private_dns"]["value"]}
    ...    scope=TEST

Connect to EC2
    Open Connection    ${EC2_PUBLIC_DNS}
    ...    timeout=30 sec
    Login With Public Key    ec2-user    examples/ec2/private_key.pem    delay=10 sec

Get Hostname
    ${output}    Execute Command    echo $HOSTNAME
    VAR    ${HOSTNAME}    ${output}    scope=TEST

Compare private DNS with Hostname
    Should Be Equal As Strings    ${HOSTNAME}    ${EC2_PRIVATE_DNS}

Destroy EC2 Instance via Terraform
    ${rc}    ${output}    Terraform Destroy    examples/ec2
    Log    ${output}
    IF    ${rc} != 0    Fail    Terraform Error:\n${output}