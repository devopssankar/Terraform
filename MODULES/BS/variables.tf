variable "application"            { type = "string" }
variable "environments"           { type = "list" }
variable "solution_stack"         { type = "string" }
variable "iam_instance_profile"   { type = "string" default = "aws-elasticbeanstalk-ec2-role" }
variable "ssh_key"                { type = "string" }
variable "instance_type"          { type = "string" }
variable "ec2_security_groups"    { type = "list" }
variable "vpc_id"                 { type = "string" }
variable "ec2_subnet_list"        { type = "list" }
variable "elb_subnet_list"        { type = "list" }
variable "iam_service_role"       { type = "string" default = "aws-elasticbeanstalk-service-role" }
variable "elb_security_groups"    { type = "list" }
variable "fqdns"                  { type = "list" }
variable "zone_id"                { type = "string" }
variable "beanstalk_elb_zone_id"  { type = "string" default = "Z117KPS5GTRQ2G" }
variable "tags"                   { type = "map" }
