terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

data "aws_iam_role" "lambda_role" {
  name = "AWSRoleForStudyLambda"
}

data "archive_file" "lambda_zip" {
  type = "zip"
  source_dir = "../../ccee-infomercado"
  output_path = "../../ccee-infomercado/ccee-infomercado.zip"
   
  excludes = [
    "terraform",
    "site-packages",
    ".git",
    ".github",
    ".gitignore",
    "site-packages.zip",
    "ccee-infomercado.zip",
    "chrome_layer.zip",
    "chrome-driver",
    "lambda_layer.zip",
    "dependencies_layer.zip",
    "__pycache__"
  ]

  
}

data "archive_file" "dependencies_layer_zip" {
  type        = "zip"
  source_dir  = "../site-packages"
  output_path = "../../ccee-infomercado/dependencies_layer.zip"

  depends_on = [
    "null_resource.dependencies_layer"
  ]
}

data "archive_file" "chrome_layer_zip" {
  type        = "zip"
  source_dir  = "../chrome-driver"
  output_path = "../chrome_layer.zip"
}

resource "null_resource" "dependencies_layer" {
  triggers = {
    timestamp = timestamp()
  }

  provisioner "local-exec" {
    command = <<EOF
      mkdir site-packages
      pip install \
          -r ./requirements.txt \
          --platform linux_x86_64 \
          --target ./site-packages/python \
          --implementation cp \
          --python-version 3.7 \
          --only-binary=:all: --upgrade
    EOF
    working_dir = "../"
  }
}

resource "aws_lambda_layer_version" "dependencies_layer" {
  filename   = data.archive_file.dependencies_layer_zip.output_path
  layer_name = "dependencies-layer"
  compatible_runtimes = ["python3.7"]
}

resource "aws_lambda_layer_version" "chrome_layer" {
  filename = data.archive_file.chrome_layer_zip.output_path
  layer_name = "chrome-layer"
  compatible_runtimes = ["python3.7"]
}

resource "aws_lambda_function" "lambda_function" {
  filename = "../ccee-infomercado.zip"
  description = "Função lambda para capturar os dados do CCEE - InfoMercado Dados Individuais"
  function_name = "lambda-ccee-infomercado-getdata"
  role = data.aws_iam_role.lambda_role.arn
  handler = "ccee_extractor.lambda_handler"
  runtime = "python3.7"
  memory_size = 2048
  timeout = 900
  layers = [aws_lambda_layer_version.dependencies_layer.arn, aws_lambda_layer_version.chrome_layer.arn]
}

# Deprecated

# resource "aws_lambda_layer_version" "chromedriver_layer" {
#   s3_bucket = "webscrapingstudy"
#   s3_key = "chromedriver/chromedriver.zip"
#   layer_name = "chromedriver-layer"
#   compatible_runtimes = ["python3.7"]
# }

# resource "aws_lambda_layer_version" "chromium_layer" {
#   s3_bucket = "webscrapingstudy"
#   s3_key = "chromedriver/headless-chromium.zip"
#   layer_name = "chromium-layer"
#   compatible_runtimes = ["python3.9"]
# }