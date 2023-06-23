variable "deploy_script_path" {
  description = "absolute path to deploy script on host"
  type        = string
}

# NOTE: not needed when deploying from deployment EC2 instance; remove in the future
#variable "aws_access_key_id" {
#  description = "AWS access key ID"
#  type        = string
#  sensitive   = true
#}
#
#variable "aws_secret_access_key" {
#  description = "AWS secret access key"
#  type        = string
#  sensitive   = true
#}
#
#variable "aws_session_token" {
#  description = "AWS session token"
#  type        = string
#  sensitive   = true
#}
#
#variable "region" {
#  description = "AWS region"
#  type        = string
#  default     = "us-west-2"
#}
