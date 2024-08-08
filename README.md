# Terraform Library for Robot Framework
[![PyPI](https://img.shields.io/pypi/v/robotframework-terraformlibrary)](https://pypi.org/project/robotframework-terraformlibrary/)[![PyPi downloads](https://img.shields.io/pypi/dm/robotframework-terraformlibrary.svg)](https://pypi.python.org/pypi/robotframework-terraformlibrary)

TerraformLibrary is a wrapper for the [Hashicorp Terraform CLI](https://developer.hashicorp.com/terraform/cli)

The library can also be configured to run [OpenTofu](https://opentofu.org/) instead of Terraform.

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

---
## Development

Install `poetry` on your system with `pip install poetry`.

Then setup the current project in a virtual env for development:

```
$ poetry env use $(which python3)
$ source $(poetry env info --path)/bin/activate
$ poetry install
```

Run the unit tests:

```
$ poetry run invoke utests
```

Run the acceptance tests:

```
$ poetry run invoke atests
```

Run all tests:

```
$ poetry run invoke tests
```

Exit the virtualenv

```
deactivate
```
---
## Releasing new versions to PyPi

To release a new version of the library to PyPi, a few steps are needed.
- update the version number in [pyproject.toml](pyproject.toml)
- rebuild the keyword documentation with the command `poetry run libdoc`
- create a pull request with the updated pyproject.toml and the keyword documentation under `docs/terraformlibrary.html`
- once the pull request is merged a new github release can be created and published which will trigger a [github action](.github/workflows/publish.yml) publishing the release to PyPi via a trusted publisher setup.