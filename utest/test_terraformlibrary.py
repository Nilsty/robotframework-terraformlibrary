import os
from pathlib import Path

import pytest

from TerraformLibrary import TerraformLibrary

testdata_directory = Path(__file__).parent.resolve() / "testdata"
terraform = TerraformLibrary()


def test_set_tf_var():
    terraform.set_tf_var("test_var", "test_value")
    assert os.environ["TF_VAR_test_var"] == "test_value"


def test_terraform_init():
    rc, output = terraform.terraform_init(f"{testdata_directory}/simple")
    assert rc == 0
    assert "Terraform has been successfully initialized!" in output


def test_terraform_plan():
    terraform.set_tf_var("my_var", "test_value")
    rc, output = terraform.terraform_plan(f"{testdata_directory}/simple")
    assert rc == 0
    assert "Terraform will perform the following actions:" in output
    assert "Plan: 1 to add, 0 to change, 0 to destroy." in output
    assert '+ my_output = "test_value"' in output


def test_terraform_apply():
    rc, output = terraform.terraform_apply(f"{testdata_directory}/simple")
    assert rc == 0
    assert "Apply complete! Resources: 1 added, 0 changed, 0 destroyed." in output
    assert 'my_output = "test_value"' in output


def test_get_terraform_state():
    output = terraform.get_terraform_state(f"{testdata_directory}/simple")
    assert output["values"]["root_module"]["resources"][0]["name"] == "foo"


def test_terraform_destroy():
    rc, output = terraform.terraform_destroy(f"{testdata_directory}/simple")
    assert rc == 0
    assert "Destroy complete! Resources: 1 destroyed." in output
    assert '- my_output = "test_value" -> null' in output


def test_terraform_error():
    rc, output = terraform.terraform_plan(f"{testdata_directory}/tf-error")
    assert rc == 1
    assert "Error: Reference to undeclared input variable" in output


def test_terraform_plan_multi_input_varfile():
    """
    Multiple inputs via a variable file.
    """
    rc, output = terraform.terraform_plan(
        f"{testdata_directory}/multi-input",
        var_files=[f"{testdata_directory}/multi-input/inputs.tfvars"],
    )
    assert rc == 0
    assert '+ output_one   = "one"' in output
    assert '+ output_two   = "two"' in output
    assert '+ output_three = "three"' in output
    assert '+ output_four  = "four"' in output
    rc, output = terraform.terraform_apply(
        f"{testdata_directory}/multi-input",
        var_files=[f"{testdata_directory}/multi-input/inputs.tfvars"],
    )
    assert rc == 0
    assert 'output_one = "one"' in output
    assert 'output_two = "two"' in output
    assert 'output_three = "three"' in output
    assert 'output_four = "four"' in output
    rc, output = terraform.terraform_destroy(
        f"{testdata_directory}/multi-input",
        var_files=[f"{testdata_directory}/multi-input/inputs.tfvars"],
    )
    assert rc == 0
    assert '- output_one   = "one" -> null' in output
    assert '- output_two   = "two" -> null' in output
    assert '- output_three = "three" -> null' in output
    assert '- output_four  = "four" -> null' in output


def test_terraform_plan_multi_input_vars():
    """
    Multiple inputs via a command line parameters.
    """
    inputs = dict(var_one="one", var_two="two", var_three="three", var_four="four")
    rc, output = terraform.terraform_plan(
        f"{testdata_directory}/multi-input", vars=inputs
    )
    assert rc == 0
    assert '+ output_one   = "one"' in output
    assert '+ output_two   = "two"' in output
    assert '+ output_three = "three"' in output
    assert '+ output_four  = "four"' in output
    rc, output = terraform.terraform_apply(
        f"{testdata_directory}/multi-input", vars=inputs
    )
    assert rc == 0
    assert 'output_one = "one"' in output
    assert 'output_two = "two"' in output
    assert 'output_three = "three"' in output
    assert 'output_four = "four"' in output
    rc, output = terraform.terraform_destroy(
        f"{testdata_directory}/multi-input", vars=inputs
    )
    assert rc == 0
    assert '- output_one   = "one" -> null' in output
    assert '- output_two   = "two" -> null' in output
    assert '- output_three = "three" -> null' in output
    assert '- output_four  = "four" -> null' in output


def test_lib_init_opentofu():
    terraform.__init__(executable="tofu")
    rc, output = terraform.terraform_init(f"{testdata_directory}/simple")
    assert rc == 0
    assert "OpenTofu has been successfully initialized!" in output
