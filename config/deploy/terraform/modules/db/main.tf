resource "aws_security_group" "dbaccess" {
  name        = "${var.prefix}-dbaccess"
  description = "Allow connecting to ${var.prefix} db"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${var.prefix}-dbaccess"
    Env  = var.prefix
  }
}

resource "aws_security_group" "db" {
  name        = "${var.prefix}-db"
  description = "Allow inbound traffic to db"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${var.prefix}-db"
    Env  = var.prefix
  }

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "TCP"
    security_groups = [aws_security_group.dbaccess.id]
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "main"
  subnet_ids = split(",", var.db_subnets)

  tags = {
    Name = "${var.prefix}-db_subnet-main"
    Env  = var.prefix
  }
}

resource "aws_db_parameter_group" "default" {
  name   = "${var.prefix}-default"
  family = "postgres14"

  tags = {
    Name = "${var.prefix}-db_params-default"
    Env  = var.prefix
  }
}

resource "aws_db_instance" "main" {
  identifier                = "${var.prefix}-main"
  allocated_storage         = 20
  storage_type              = "gp2"
  engine                    = "postgres"
  engine_version            = "14.2"
  instance_class            = "db.t3.micro"
  parameter_group_name      = aws_db_parameter_group.default.name
  vpc_security_group_ids    = [aws_security_group.db.id]
  final_snapshot_identifier = "${var.prefix}-${md5(timestamp())}"
  db_subnet_group_name      = aws_db_subnet_group.main.id

  db_name  = "main"
  username = "ncfe_newable"
  password = var.db_password

  tags = {
    Name = "${var.prefix}-main"
    Env  = var.prefix
  }
}
