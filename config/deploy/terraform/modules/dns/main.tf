data "aws_region" "current" {}

resource "aws_route53_zone" "main" {
  name = var.domain_name

  tags = {
    Name = "${var.prefix}-main"
    Env  = var.prefix
  }
}

resource "aws_route53_record" "main_elasticbeanstalk" {
  zone_id = aws_route53_zone.main.id
  name    = "www.${aws_route53_zone.main.name}"
  type    = "A"

  alias {
    name                   = var.app_cname
    zone_id                = var.elb_hosted_zones[data.aws_region.current.name]
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "main_www_alias" {
  zone_id = aws_route53_zone.main.id
  name    = aws_route53_zone.main.name
  type    = "A"

  alias {
    name                   = "www.${aws_route53_zone.main.name}"
    zone_id                = aws_route53_zone.main.id
    evaluate_target_health = false
  }

  depends_on = [aws_route53_record.main_elasticbeanstalk]
}
