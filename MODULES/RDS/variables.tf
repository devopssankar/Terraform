variable "name"              { type = "string" }
variable "vpc_id"            { type = "string" }
variable "db_name"           { type = "string" }
variable "db_user"           { type = "string" }
variable "db_password"       { type = "string" }
variable "final_snapshot"    { type = "boolean" default = true }
variable "db_family"         { type = "string" default = "aurora5.6"}
variable "db_subnet_list"    { type = "list" }
variable "db_instance_count" { type = "string" default = "1" }
variable "db_instance_type"  { type = "string" default = "db.t2.small" }
variable "tags"              { type = "map" }