terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Bucket S3 para backup periódico do inventário exportado pela StockAPI
resource "aws_s3_bucket" "inventario_backup" {
  bucket = "stockapi-inventario-backup"

  tags = {
    Name        = "stockapi-inventario-backup"
    Environment = "production"
    Project     = "StockAPI"
  }
}

resource "aws_s3_bucket_public_access_block" "inventario_backup" {
  bucket = aws_s3_bucket.inventario_backup.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "inventario_backup" {
  bucket = aws_s3_bucket.inventario_backup.id

  versioning_configuration {
    status = "Enabled"
  }
}
