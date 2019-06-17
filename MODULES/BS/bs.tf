resource "aws_elastic_beanstalk_environment" "bs" {
  name                      = "${format("%s-%s", var.application, element(var.environments, count.index))}"
  application               = "${var.application}"
  solution_stack_name       = "${var.solution_stack}"
  count                     = "${length(var.environments)}"
  setting {
    namespace               = "aws:autoscaling:asg"
    name                    = "Availability Zones"
    value                   = "Any 1"
  }
  setting {
    namespace               = "aws:autoscaling:asg"
    name                    = "MinSize"
    value                   = "1"
  }
  setting {
    namespace               = "aws:autoscaling:asg"
    name                    = "MaxSize"
    value                   = "1"
  }
  setting {
    namespace               = "aws:autoscaling:launchconfiguration"
    name                    = "IamInstanceProfile"
    value                   = "${var.iam_instance_profile}"
  }
  setting {
    namespace               = "aws:autoscaling:launchconfiguration"
    name                    = "EC2KeyName"
    value                   = "${var.ssh_key}"
  }
  setting {
    namespace               = "aws:autoscaling:launchconfiguration"
    name                    = "InstanceType"
    value                   = "${var.instance_type}"
  }
  setting {
    namespace               = "aws:autoscaling:launchconfiguration"
    name                    = "SecurityGroups"
    value                   = "${join(",",var.ec2_security_groups)}"
  }
  setting {
    namespace               = "aws:autoscaling:updatepolicy:rollingupdate"
    name                    = "RollingUpdateEnabled"
    value                   = "true"
  }
  setting {
    namespace               = "aws:autoscaling:updatepolicy:rollingupdate"
    name                    = "RollingUpdateType"
    value                   = "Health"
  }
  setting {
    namespace               = "aws:autoscaling:updatepolicy:rollingupdate"
    name                    = "MinInstancesInService"
    value                   = "0"
  }
  setting {
    namespace               = "aws:autoscaling:updatepolicy:rollingupdate"
    name                    = "MaxBatchSize"
    value                   = "1"
  }  
  setting {
    namespace               = "aws:ec2:vpc"
    name                    = "VPCId"
    value                   = "${var.vpc_id}"
  }
  setting {
    namespace               = "aws:ec2:vpc"
    name                    = "AssociatePublicIpAddress"
    value                   = "false"
  }
  setting {
    namespace               = "aws:ec2:vpc"
    name                    = "Subnets"
    value                   = "${join(",",var.ec2_subnet_list)}"
  }
  setting {
    namespace               = "aws:ec2:vpc"
    name                    = "ELBSubnets"
    value                   = "${join(",",var.elb_subnet_list)}"
  }
  setting {
    namespace               = "aws:ec2:vpc"
    name                    = "ELBScheme"
    value                   = "internal"
  }
  setting {
    namespace               = "aws:elasticbeanstalk:application:environment"
    name                    = "environment"
    value                   = "${element(var.environments, count.index)}"
  }
  setting {
    namespace               = "aws:elasticbeanstalk:application:environment"
    name                    = "LOGGING_APPENDER"
    value                   = "GRAYLOG"
  }
  setting {
    namespace               = "aws:elasticbeanstalk:command"
    name                    = "BatchSizeType"
    value                   = "Fixed"
  }
  setting {
    namespace               = "aws:elasticbeanstalk:command"
    name                    = "BatchSize"
    value                   = "1"
  }
  setting {
    namespace               = "aws:elasticbeanstalk:command"
    name                    = "DeploymentPolicy"
    value                   = "Rolling"
  }
  setting {
    namespace               = "aws:elasticbeanstalk:environment"
    name                    = "ServiceRole"
    value                   = "${var.iam_service_role}"
  }
  setting {
    namespace               = "aws:elasticbeanstalk:healthreporting:system"
    name                    = "SystemType"
    value                   = "enhanced"
  }
  setting {
    namespace               = "aws:elb:listener:80"
    name                    = "ListenerProtocol"
    value                   = "HTTP"
  }
  setting {
    namespace               = "aws:elb:listener:80"
    name                    = "InstanceProtocol"
    value                   = "HTTP"
  }
  setting {
    namespace               = "aws:elb:listener:80"
    name                    = "InstancePort"
    value                   = "80"
  }
  setting {
    namespace               = "aws:elb:listener:443"
    name                    = "ListenerEnabled"
    value                   = "false"
  }
  setting {
    namespace               = "aws:elb:loadbalancer"
    name                    = "CrossZone"
    value                   = "false"
  }
  setting {
    namespace               = "aws:elb:loadbalancer"
    name                    = "SecurityGroups"
    value                   = "${join(",", var.elb_security_groups)}"
  }
  setting {
    namespace               = "aws:elb:policies"
    name                    = "ConnectionDrainingEnabled"
    value                   = "true"
  }
  tags                      = "${merge(var.tags, map("Name", format("apm-%s-%s", lookup(var.tags, "Cluster"), element(var.environments, count.index))))}"
  lifecycle {
    ignore_changes          = ["tags"]
  }
}
resource "aws_route53_record" "fqdn" {
  depends_on                = ["aws_elastic_beanstalk_environment.bs"]
  count                     = "${length(var.fqdns)}"
  zone_id                   = "${var.zone_id}"
  name                      = "${element(var.fqdns, count.index)}"
  type                      = "A"
  alias {
    name                    = "${element(aws_elastic_beanstalk_environment.bs.*.cname, count.index)}"
    zone_id                 = "${var.beanstalk_elb_zone_id}"
    evaluate_target_health  = false
  }
}
