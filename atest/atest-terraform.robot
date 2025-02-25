*** Settings ***
Library    TerraformLibrary

*** Variables ***
${TESTDATA}    ${CURDIR}/testdata

*** Test Cases ***
Run Terraform Init
    ${rc}    ${output}    Terraform Init    ${TESTDATA}/simple
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${output}    Terraform has been successfully initialized!

Run Terraform Plan
    Set TF Var    my_var    test_value
    ${rc}    ${output}    Terraform Plan    ${TESTDATA}/simple
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${output}    Plan: 1 to add, 0 to change, 0 to destroy.
    Should Contain    ${output}    + my_output = "test_value"

Run Terraform Plan With Var File
    ${rc}    ${output}    Terraform Plan    ${TESTDATA}/multi-input    var_files=["${TESTDATA}/multi-input/inputs.tfvars"]
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${output}    + output_one   = "one"
    Should Contain    ${output}    + output_two   = "two"
    Should Contain    ${output}    + output_three = "three"
    Should Contain    ${output}    + output_four  = "four"

Run Terraform Plan With Variable Inputs
    &{inputs}    Create Dictionary    var_one=one    var_two=two    var_three=three    var_four=four
    ${rc}    ${output}    Terraform Plan    ${TESTDATA}/multi-input    vars=${inputs}
    Should Be Equal As Integers    ${rc}    0
    Should Contain    ${output}    + output_one   = "one"
    Should Contain    ${output}    + output_two   = "two"
    Should Contain    ${output}    + output_three = "three"
    Should Contain    ${output}    + output_four  = "four"

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