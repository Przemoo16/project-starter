variable "prefix" {}
variable "domain_name" {}
variable "app_cname" {}

# http://docs.aws.amazon.com/general/latest/gr/rande.html#elasticbeanstalk_region
# don't change. it's static.
variable "elb_hosted_zones" {
  type = map(string)
  default = {
    "us-east-2"      = "Z14LCN19Q5QHIC"
    "us-east-1"      = "Z117KPS5GTRQ2G"
    "us-west-1"      = "Z1LQECGX5PH1X"
    "us-west-2"      = "Z38NKT9BP95V3O"
    "ca-central-1"   = "ZJFCZL7SSZB5I"
    "ap-south-1"     = "Z18NTBI3Y7N9TZ"
    "ap-northeast-2" = "Z3JE5OI70TWKCP"
    "ap-southeast-1" = "Z16FZ9L249IFLT"
    "ap-southeast-2" = "Z2PCDNR3VC2G1N"
    "ap-northeast-1" = "Z1R25G3KIG2GBW"
    "eu-central-1"   = "Z1FRNW7UH4DEZJ"
    "eu-west-1"      = "Z2NYPWQ7DFZAZH"
    "eu-west-2"      = "Z1GKAAAUGATPF1"
    "sa-east-1"      = "Z10X7K2B4QSOFV"
  }
}
