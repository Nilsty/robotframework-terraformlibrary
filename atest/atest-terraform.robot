*** Settings ***
Library    TerraformLibrary

*** Variables ***
${TESTDATA}    ${CURDIR}/testdata

*** Test Cases ***
Run Terraform Init
    ${rc}    ${output}    Terraform Init    ${TESTDATA}/simple
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${output}    has been successfully initialized!

Run Terraform Plan
    Set TF Var    my_var    test_value
    ${rc}    ${output}    Terraform Plan    ${TESTDATA}/simple
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${output}    Plan: 1 to add, 0 to change, 0 to destroy.
    Should Contain    ${output}    + my_output = "test_value"

Run Terraform Apply
    ${rc}    ${output}    Terraform Apply    ${TESTDATA}/simple
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${output}    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    Should Contain    ${output}    my_output = "test_value"

Inspect Terraform State
    ${output}    Get Terraform State    ${TESTDATA}/simple
    Should Be Equal As Strings    ${output["values"]["root_module"]["resources"][0]["name"]}    foo

Run Terraform Destroy
    ${rc}    ${output}    Terraform Destroy    ${TESTDATA}/simple
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${output}    Destroy complete! Resources: 1 destroyed.
    Should Contain    ${output}    - my_output = "test_value" -> null

Terraform Error Is Raised
    ${rc}    ${output}    Terraform Plan    ${TESTDATA}/tf-error
    Should Be Equal As Integers    ${rc}    1
    Should Contain    ${output}    Error: Reference to undeclared input variable