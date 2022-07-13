#!/bin/bash
# AWS Regions ("us-east-1" "us-east-2" "us-west-1" "us-west-2" "eu-west-1" "eu-central-1" "ap-northeast-1" "ap-northeast-2" "ap-southeast-1" "ap-southeast-2" "ap-south-1" "sa-east-1")

aws_default_region="us-east-1"
declare -a aws_additional_regions=("us-east-2" "us-west-1" "us-west-2" "ap-northeast-1" "ap-southeast-1")

terraform workspace select default

echo "=============== Multi-Region Deployment List ==============="
terraform workspace list

for aws_region in "${aws_additional_regions[@]}"
do
    echo "\n============================================================"
    echo "Destroy in region: $aws_region"
    echo "============================================================"
    terraform workspace select $aws_region || break;
    terraform destroy -var "aws_region=$aws_region" || break;
done

terraform workspace select default

echo "============================================================"
echo "Destroy in default region: $aws_default_region"
echo "============================================================"
terraform destroy -var "aws_region=$aws_default_region" || exit 1
