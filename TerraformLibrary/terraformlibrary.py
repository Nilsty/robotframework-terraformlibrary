"""
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

"""

import json
import os
import subprocess
from importlib.metadata import version

from robot.api import logger
from robot.api.deco import library

try:
    __version__ = version("robotframework-terraformlibrary")
except Exception:
    pass


@library(scope="GLOBAL", version=__version__, auto_keywords=True)
class TerraformLibrary:
    """
    The Terraform Library is a wrapper for the Terraform CLI.

    With the integration of Terraform into Robot Framework, inputs can be passed from tests to terraform executions and outputs from
    terraform script can be used in robot tests. Commands like ``terraform init``, ``plan``, ``apply`` and ``destroy`` can be used
    with any terraform script.

    """

    def __init__(self, executable="terraform"):
        """
        The TerraformLibrary can either use the terraform executable (default) or can be configured
        to run OpenTofu instead by setting the executable to `tofu`. https://opentofu.org/
        | ***** Settings *****
        | Library    TerraformLibrary    executable=tofu
        """
        self.exec = executable

    def _run_command(self, command: str, include_stderr: bool = False):
        process = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=(subprocess.STDOUT if include_stderr else subprocess.PIPE),
        )
        output = process.stdout.decode()
        rc = process.returncode
        if process.stderr:
            logger.write("stderr = " + process.stderr.decode())
        return rc, output

    def terraform_init(self, script_path: str):
        """
        ``terraform init``
        Initialize your terraform working directory and download any needed providers.

        https://developer.hashicorp.com/terraform/cli/commands/init

        Example:
        | ${rc} | ${output} | Terraform Init | ${PATH_TO_TERRAFORM_SCRIPT} |

        Returns the return code and the output of the terraform command.
        """
        command = f"{self.exec} -chdir={script_path} init -no-color"
        rc, output = self._run_command(command, include_stderr=True)
        return rc, output

    def terraform_plan(self, script_path: str):
        """
        ``terraform plan``
        Create the terraform plan.

        https://developer.hashicorp.com/terraform/cli/commands/plan

        Example:
        | ${rc} | ${output} | Terraform Plan | ${PATH_TO_TERRAFORM_SCRIPT} |

        Returns the return code and the output of the terraform command.
        """
        command = f"{self.exec} -chdir={script_path} plan -no-color -input=false"
        rc, output = self._run_command(command, include_stderr=True)
        return rc, output

    def terraform_apply(self, script_path: str):
        """
        ``terraform apply``
        Applies the terraform plan and creates resources.

        https://developer.hashicorp.com/terraform/cli/commands/apply

        Example:
        | ${rc} | ${output} | Terraform Apply | ${PATH_TO_TERRAFORM_SCRIPT} |

        Returns the return code and the output of the terraform command.
        """
        command = f"{self.exec} -chdir={script_path} apply -auto-approve -no-color -input=false"
        rc, output = self._run_command(command, include_stderr=True)
        return rc, output

    def terraform_destroy(self, script_path: str):
        """
        ``terraform destroy``
        Destroys the applied resources.

        https://developer.hashicorp.com/terraform/cli/commands/destroy

        Example:
        | ${rc} | ${output} | Terraform Destroy | ${PATH_TO_TERRAFORM_SCRIPT} |

        Returns the return code and the output of the terraform command.
        """
        command = f"{self.exec} -chdir={script_path} destroy -auto-approve -no-color -input=false"
        rc, output = self._run_command(command, include_stderr=True)
        return rc, output

    def set_tf_var(self, name: str, value: str):
        """
        Set an environment variable with the prefix TF_VAR_.
        Due to the prefix this environment variables will become available to the terraform execution.

        https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_var_name

        Example:
        | Set TF Var | my_var_name | my var value |

        This will set the environment variable `TF_VAR_my_var_name`.
        Which will be available as an input to the terraform script as `my_var_name`.
        """
        prefix = "TF_VAR_"
        os.environ[f"{prefix}{name}"] = f"{value}"

    def get_terraform_state(self, script_path: str):
        """
        Get Terraform State will execute the command `terraform show --json`.
        This will make the terraform state available as a JSON object.

        https://developer.hashicorp.com/terraform/cli/commands/show

        Example:
        | ${TF_state_json} | Get Terraform State | ${PATH_TO_TERRAFORM_SCRIPT} |
        | Should Be Equal As Strings | ${output["values"]["root_module"]["resources"][0]["name"]} | name of the first resource |

        """
        command = f"{self.exec} -chdir={script_path} show -json"
        rc, output = self._run_command(command)
        try:
            output_json = json.loads(output)
            return output_json
        except:
            logger.warn("output not in json format")
            return output
