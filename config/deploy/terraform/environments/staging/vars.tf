variable "application_environment" {
  description = "Deployment stage e.g. 'staging', 'production', 'test', 'integration'"
}

variable "prefix" {
  description = "Prefix for env resources"
}

variable "key_pair_name" {
  description = "Key pair used to access AWS instance"
}

variable "domain_name" {
  description = "Domain to be used by application"
}

variable "app_name" {
  description = "Name of the application"
}

variable "smtp_host" {
  description = "Host of the email service"
}

variable "smtp_port" {
  description = "Port of the email service"
}

variable "smtp_user" {
  description = "User of the email service"
}

variable "email_sender" {
  description = "Email sender used by the email service"
}

##########################
# Read from secrets.tfvar
##########################
variable "db_password" {
  description = "Password for main DB"
}

variable "secret_key" {
  description = "Secret key for the web application"
}

variable "smtp_password" {
  description = "Password of the SMTP email service"
}

variable "sentry_dsn" {
  description = "The DSN tells the SDK where to send the events to"
}
