remote_state {
  backend = "s3"

  config = {
    bucket         = "project-starter"
    region         = "eu-central-1"
    encrypt        = true
    key            = "project-starter/${path_relative_to_include()}/terraform.tfstate"
    dynamodb_table = "project-starter-dynamodb"
  }
}

terraform {
  extra_arguments "secrets" {
    arguments = [
      "-var-file=${get_terragrunt_dir()}/secrets.tfvars"
    ]
    commands = [
      "apply",
      "plan",
      "destroy",
      "import",
      "push",
      "refresh"
    ]
  }
}
