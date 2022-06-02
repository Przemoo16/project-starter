output "dbaccess_sg_id" {
  value = aws_security_group.dbaccess.id
}

output "db_endpoint" {
  value = aws_db_instance.main.endpoint
}

output "db_name" {
  value = aws_db_instance.main.name
}

output "db_port" {
  value = aws_db_instance.main.port
}

output "db_username" {
  value = aws_db_instance.main.username
}
