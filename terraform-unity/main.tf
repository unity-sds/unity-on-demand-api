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
  command = [
    "/tmp/deploy.sh"
  ]
  volumes {
    host_path      = var.deploy_script_path
    container_path = "/tmp/deploy.sh"
  }
}
