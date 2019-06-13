data "aws_acm_certificate" "elb" {
  domain                    = "${var.domain_cert}"
  statuses                  = ["ISSUED"]
}
resource "aws_elb" "elb" {
  name                      = "${var.elbname}"
  instances                 = ["${var.backend_instances}"]
  internal                  = "${var.elbplacement}"
  subnets                   = ["${var.subnets_list}"]
  security_groups           = ["${var.security_groups}"]
 listener {
    instance_port           = "${var.instance_port}"
    instance_protocol       = "${var.instance_protocol}"
    lb_port                 = "${var.lb_port}"
    lb_protocol             = "${var.lb_protocol}"
    ssl_certificate_id      = "${data.aws_acm_certificate.elb.arn}"
  }
  health_check {
    healthy_threshold       = "${var.healthy_threshold}"
    unhealthy_threshold     = "${var.unhealthy_threshold}"
    timeout                 = "${var.timeout}"
    target                  = "${var.target}"
    interval                = "${var.interval}"
  }
  lifecycle {
    create_before_destroy   = true
  }
  tags                      = "${merge(var.tags)}"
}
resource "aws_load_balancer_policy" "service-ssl" {
  load_balancer_name        = "${aws_elb.elb.name}"
  policy_name               = "service-ssl"
  policy_type_name          = "SSLNegotiationPolicyType"
  policy_attribute = {
    name                    = "ECDHE-ECDSA-AES128-GCM-SHA256"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "ECDHE-RSA-AES128-GCM-SHA256"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "ECDHE-ECDSA-AES128-SHA256"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "ECDHE-RSA-AES128-SHA256"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "ECDHE-ECDSA-AES256-GCM-SHA384"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "ECDHE-RSA-AES256-GCM-SHA384"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "ECDHE-ECDSA-AES256-SHA384"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "ECDHE-RSA-AES256-SHA384"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "AES128-GCM-SHA256"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "AES128-SHA256"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "AES256-GCM-SHA384"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "AES256-SHA256"
    value                   = "true"
  }
  policy_attribute = {
    name                    = "Protocol-TLSv1.2"
    value                   = "true"
  }
}
resource "aws_load_balancer_listener_policy" "service-listener-policies-443" {
  load_balancer_name        = "${aws_elb.elb.name}"
  load_balancer_port        = 443
  policy_names              = ["${aws_load_balancer_policy.service-ssl.policy_name}"]
}
resource "aws_route53_record" "fqdn" {
  zone_id                   = "${var.zone_id}"
  name                      = "${var.service_fqdn}"
  type                      = "A"
  alias {
    name                    = "${aws_elb.elb.dns_name}"
    zone_id                 = "${aws_elb.elb.zone_id}"
    evaluate_target_health  = false
  }
}
output "fqdn" { value = "${aws_route53_record.fqdn.*.id}" }
