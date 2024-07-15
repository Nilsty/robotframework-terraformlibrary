
# Terraform Library for Robot Framework

The TerraformLibrary is a wrapper for the Hashicorp Terraform CLI

With the integration of Terraform into Robot Framework, inputs can be passed from tests to terraform executions and outputs from 
terraform script can be used in robot tests. Commands like ``terraform init``, ``plan``, ``apply`` and ``destroy`` can be used 
with any terraform script. 

https://developer.hashicorp.com/terraform/cli

---
## Keyword Documentation
[Link to the keyword documentation](https://nilsty.github.io/robotframework-terraformlibrary/terraformlibrary.html)

---
## Installation
If you already have Python >= 3.8 with pip installed, you can simply run:  
`pip install --upgrade robotframework-terraformlibrary`

---
## Getting started
Some examples how to import and use the library.

``` robotframework
*** Settings ***
Library            TerraformLibrary

*** Variables ***
${PATH_TO_TERRAFORM_SCRIPT}    ${CURDIR}/terraform-script

*** Test Cases ***
Run Terraform Init
    ${rc}    ${output}    Terraform Init    ${PATH_TO_TERRAFORM_SCRIPT}

Run Terraform Plan
    Set TF Var    my_var    test_value
    ${rc}    ${output}    Terraform Plan    ${PATH_TO_TERRAFORM_SCRIPT}
    Should Contain    ${output}    Plan: 1 to add, 0 to change, 0 to destroy.

Run Terraform Apply
    ${rc}    ${output}    Terraform Apply    ${PATH_TO_TERRAFORM_SCRIPT}
    Should Contain    ${output}    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Inspect Terraform State
    ${output}    Get Terraform State    ${PATH_TO_TERRAFORM_SCRIPT}
    Should Be Equal As Strings    ${output["values"]["root_module"]["resources"][0]["name"]}    foo

Run Terraform Destroy
    ${rc}    ${output}    Terraform Destroy    ${PATH_TO_TERRAFORM_SCRIPT}
    Should Contain    ${output}    Destroy complete! Resources: 1 destroyed.
```

