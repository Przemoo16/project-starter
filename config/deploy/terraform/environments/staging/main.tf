terraform {
  # The configuration for this backend will be filled in by Terragrunt
  backend "s3" {}
}

provider "aws" {
  region = "eu-central-1"
}

module "application" {
  source                  = "../../modules/app"
  application_environment = var.application_environment
  prefix                  = var.prefix
  key_pair_name           = var.key_pair_name
  domain_name             = var.domain_name
  db_password             = var.db_password
  secret_key              = var.secret_key
  app_name                = var.app_name
  smtp_host               = var.smtp_host
  smtp_port               = var.smtp_port
  smtp_user               = var.smtp_user
  smtp_password           = var.smtp_password
  email_sender            = var.email_sender
  sentry_dsn              = var.sentry_dsn
}
