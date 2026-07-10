terraform {
  backend "s3" {
    bucket       = "serhan-plus-one-terraform-state-2026"
    key          = "plus-one/terraform.tfstate"
    region       = "eu-west-2"
    use_lockfile = true
  }
}