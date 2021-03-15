module github.com/ku-spent/serverless-stack/personalize-service/api

go 1.16

require (
	github.com/aws/aws-lambda-go v1.22.0
	github.com/aws/aws-sdk-go-v2/config v1.1.1
	github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue v1.0.2
	github.com/aws/aws-sdk-go-v2/feature/dynamodb/expression v1.0.2
	github.com/aws/aws-sdk-go-v2/service/dynamodb v1.1.1
	github.com/aws/aws-sdk-go-v2/service/personalizeruntime v1.1.1
	github.com/awslabs/aws-lambda-go-api-proxy v0.9.0
	github.com/gin-gonic/gin v1.6.3
	github.com/google/go-querystring v1.0.0 // indirect
	github.com/pkg/errors v0.9.1
	github.com/stretchr/testify v1.7.0 // indirect
)
