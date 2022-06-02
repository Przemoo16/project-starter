resource "aws_default_route_table" "main" {
  default_route_table_id = aws_vpc.main.default_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main_gw.id
  }

  tags = {
    Name = "${var.prefix}-main"
    Env  = var.prefix
  }
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "${var.prefix}-main"
    Env  = var.prefix
  }
}

resource "aws_internet_gateway" "main_gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.prefix}-main-gw"
    Env  = var.prefix
  }
}

resource "aws_subnet" "main_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = "eu-central-1a"

  tags = {
    Name = "${var.prefix}-main-subnet-a"
    Env  = var.prefix
  }
}

resource "aws_subnet" "main_b" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-central-1b"

  tags = {
    Name = "${var.prefix}-main-subnet-b"
    Env  = var.prefix
  }
}

resource "aws_subnet" "main_c" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-central-1c"

  tags = {
    Name = "${var.prefix}-main-subnet-c"
    Env  = var.prefix
  }
}

resource "aws_security_group" "web" {
  name        = "${var.prefix}-web"
  description = "Allow connecting to instances ${var.prefix}"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.prefix}-web"
    Env  = var.prefix
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ssh" {
  name        = "${var.prefix}-ssh"
  description = "Allow connecting via ssh ${var.prefix}"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.prefix}-ssh"
    Env  = var.prefix
  }

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "TCP"

    cidr_blocks = [
      "109.173.173.179/32",
    ]
  }
}
