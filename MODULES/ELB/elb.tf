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
