terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.84.0"
    }
  }
}

provider "aws" {
  region  = "eu-central-1"
  profile = "default"
}

resource "aws_instance" "robot_ec2_instance" {
  ami             = "ami-0cdd6d7420844683b"
  instance_type   = "t2.micro"
  key_name        = var.aws_ssh_key
  subnet_id       = var.subnet
  security_groups = [var.security_group]
  tags = {
    Name = "Robot-Example-Instance"
  }
  provisioner "local-exec" {
    command = "aws ec2 wait instance-running --profile=default --instance-ids ${self.id}"
  }
}

output "instance_public_dns" {
  description = "Public Ip of the EC2 instance"
  value       = aws_instance.robot_ec2_instance.public_dns
}

output "instance_private_dns" {
  description = "Public Ip of the EC2 instance"
  value       = aws_instance.robot_ec2_instance.private_dns
}

# Input Variables
variable "aws_ssh_key" {
  description = "SSH Key stored in AWS account"
  type        = string
}

variable "subnet" {
  description = "Subnet for EC2 Instance"
  type        = string
}

variable "security_group" {
  description = "Security Group for EC2 Instance"
  type        = string
}