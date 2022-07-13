#!/bin/bash
# AWS Regions ("us-east-1" "us-east-2" "us-west-1" "us-west-2" "eu-west-1" "eu-central-1" "ap-northeast-1" "ap-northeast-2" "ap-southeast-1" "ap-southeast-2" "ap-south-1" "sa-east-1")

aws_default_region="us-east-1"
declare -a aws_additional_regions=("us-east-2" "us-west-1" "us-west-2" "ap-northeast-1" "ap-southeast-1")

terraform workspace select default

echo "=============== Multi-Region Deployment List ==============="
terraform workspace list

echo "============================================================"
echo "Deploying in default region: $aws_default_region"
echo "============================================================"
terraform apply -var "aws_region=$aws_default_region" || exit 1

for aws_region in ${aws_additional_regions[@]}
do
    echo "\n============================================================"
    echo "Deploying in region: $aws_region"
    echo "============================================================"
    terraform workspace new $aws_region
    terraform workspace select $aws_region
    terraform apply -var "aws_region=$aws_region" --auto-approve || break;
done

terraform workspace select default
