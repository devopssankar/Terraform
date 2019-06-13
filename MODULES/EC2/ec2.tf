resource "aws_instance" "ec2" {
  count                       = "${var.ins_count}"
  ami                         = "${var.image_id}"
  instance_type               = "${var.ins_type}"
  key_name                    = "${var.key_name}"
  subnet_id                   = "${var.subnet_id}"
  ebs_optimized               = "${var.optmizeebs}"
  associate_public_ip_address = "${var.publicip}"
  disable_api_termination     = "${var.protection}"
  iam_instance_profile        = "${var.iam_profile}"
  vpc_security_group_ids      = ["${var.ec2sg}"]
  root_block_device {
    volume_size               = "${var.vol_size}"
    volume_type               = "gp2"
  }
  user_data                   = "${var.userdata}"
  lifecycle {
    ignore_changes            = ["user_data"]
  }
  tags                        = "${merge(var.tags)}"
}
output "instance_id" { value = "${aws_instance.ec2.*.id}" }
output "instance_ip" { value = "${aws_instance.ec2.*.private_ip}" }
