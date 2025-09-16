variable "project_id" {
    default = "padel-app"
}

variable "region" {
  default = "europe-west1"
}

variable "zone" {
  default = "europe-west1-b"
}

variable "postgres_password" {
  description = "Password for Postgres user padel_app_user"
  type        = string
  sensitive   = true
}