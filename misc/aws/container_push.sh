# Create ECR (if not already existing)
aws ecr create-repository --repository-name "selfie2anime-api"

ACCOUNT_ID=$(aws sts get-caller-identity |  jq -r '.Account')
$(aws ecr get-login --no-include-email --region ap-southeast-2)

docker build -t selfie2anime-api ../../
docker tag selfie2anime-api:latest $ACCOUNT_ID.dkr.ecr.ap-southeast-2.amazonaws.com/selfie2anime-api:latest
docker push $ACCOUNT_ID.dkr.ecr.ap-southeast-2.amazonaws.com/selfie2anime-api:latest