variable "var_one" {
  type  = string
}
variable "var_two" {
  type  = string
}
variable "var_three" {
  type  = string
}
variable "var_four" {
  type  = string
}

output "output_one" {
  value = var.var_one
}
output "output_two" {
  value = var.var_two
}
output "output_three" {
  value = var.var_three
}
output "output_four" {
  value = var.var_four
}
