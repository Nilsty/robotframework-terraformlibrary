# TF script causing an error

output "out" {
  # Generate an error at runtime by evaluating a regex late
  value =  regex(var.in == null ? "invalid(" : "invalid(", "input")
}
