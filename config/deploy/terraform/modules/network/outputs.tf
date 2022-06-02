output "vpc_id" {
  value = aws_vpc.main.id
}

output "ssh_access_sg_id" {
  value = aws_security_group.ssh.id
}

output "web_access_sg_id" {
  value = aws_security_group.web.id
}

output "subnets" {
  value = [
    aws_subnet.main_a.id,
    aws_subnet.main_b.id,
    aws_subnet.main_c.id,
  ]
}
