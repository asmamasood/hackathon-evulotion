# Backend configuration for Terraform state management

terraform {
  backend "s3" {
    bucket         = "todo-app-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "todo-app-terraform-locks"
  }
}