terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "2.5.1"
    }
  }
}

resource "local_file" "foo" {
  content  = "foo!"
  filename = "${path.module}/foo.bar"
}

variable "my_var" {
  type  = string
}

output "my_output" {
  value = var.my_var
}
