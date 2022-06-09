include {
  path = find_in_parent_folders()
}

inputs = {
  application_environment = "staging"
  prefix = "project-starter-staging"
  key_pair_name = "project-starter"
  domain_name = "test-staging.zxc123.eu-central-1.elasticbeanstalk.com"
  smtp_host = "SMTP_HOST"
  smtp_port = 465
  smtp_user = "SMTP_USER"
  email_sender = "test@email.com"
}
