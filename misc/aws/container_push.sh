MODEL_NAME="selfie2anime"

# Create ECR (if not already existing)
aws ecr create-repository --repository-name "$MODEL_NAME-api"

ACCOUNT_ID=$(aws sts get-caller-identity |  jq -r '.Account')
$(aws ecr get-login --no-include-email --region ap-southeast-2)

docker build -t $MODEL_NAME-api ../../
docker tag $MODEL_NAME-api:latest $ACCOUNT_ID.dkr.ecr.ap-southeast-2.amazonaws.com/$MODEL_NAME-api:latest
docker push $ACCOUNT_ID.dkr.ecr.ap-southeast-2.amazonaws.com/$MODEL_NAME-api:latest
