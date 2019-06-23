#RDS SG
resource "aws_security_group" "db" {
  name                    = "${var.name}-db"
  vpc_id                  = "${var.vpc_id}"
  tags                    = "${merge(var.tags)}"
  egress {
    from_port             = 0
    to_port               = 0
    protocol              = "-1"
    cidr_blocks           = ["0.0.0.0/0"]
  }
}
resource "aws_rds_cluster" "rds" {
  cluster_identifier      = "${var.name}-db"
  db_subnet_group_name    = "${aws_db_subnet_group.rds.name}"
  vpc_security_group_ids  = ["${aws_security_group.db.id}"]
  database_name           = "${var.db_name}"
  master_username         = "${var.db_user}"
  master_password         = "${var.db_password}"
  skip_final_snapshot     = "${var.final_snapshot}"
  backup_retention_period = 5
  preferred_backup_window = "07:00-09:00"
  lifecycle {
    create_before_destroy = true
  }
}
resource "aws_db_parameter_group" "rds" {
  name                    = "${var.name}-db-pg"
  family                  = "${var.db_family}"
  parameter {
    name                  = "max_connections"
    value                 = "550"
  }
}
resource "aws_db_subnet_group" "rds" {
  name                    = "${var.name}-db-subnetgroup"
  subnet_ids              = ["${var.db_subnet_list}"]
  tags                    = "${merge(var.tags)}"
  lifecycle {
    create_before_destroy = true
  }
}
resource "aws_rds_cluster_instance" "rds" {
  count                   = "${var.db_instance_count}"
  identifier              = "${var.name}-db-${count.index}"
  cluster_identifier      = "${aws_rds_cluster.rds.id}"
  db_subnet_group_name    = "${aws_db_subnet_group.rds.name}"
  instance_class          = "${var.db_instance_type}"
  tags                    = "${merge(var.tags)}"
  lifecycle {
    create_before_destroy = true
  }
}
output "db_secgroup" { value = "${aws_security_group.db.id}"}
output "db_hostname" { value = "${aws_rds_cluster.rds.endpoint}" }
output "db_username" { value = "${aws_rds_cluster.rds.master_username}" }
output "db_password" { value = "${var.db_password}" }
output "db_database" { value = "${aws_rds_cluster.rds.database_name}" }
