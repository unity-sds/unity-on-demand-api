terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.23.1"
    }
  }
}

resource "docker_image" "node" {
  name = "node:16.20.0"
}

resource "docker_container" "serverless" {
  image      = docker_image.node.image_id
  name       = "terraform-docker-test"
  must_run   = false
  entrypoint = ["/bin/bash"]
  # NOTE: not needed when deploying from deployment EC2 instance; remove in the future
  #env = [
  #  "AWS_ACCESS_KEY_ID=${var.aws_access_key_id}",
  #  "AWS_SECRET_ACCESS_KEY=${var.aws_secret_access_key}",
  #  "AWS_SESSION_TOKEN=${var.aws_session_token}",
  #  "AWS_DEFAULT_REGION=${var.region}"
  #]
  command = [
    "/tmp/deploy.sh"
  ]

  volumes {
    host_path      = var.deploy_script_path
    container_path = "/tmp/deploy.sh"
  }
}
