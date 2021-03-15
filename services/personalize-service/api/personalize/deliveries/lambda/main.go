package main

import (
	"context"
	"log"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	ginadapter "github.com/awslabs/aws-lambda-go-api-proxy/gin"
	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/configs"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/helpers"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/router"
)

var ginLambda *ginadapter.GinLambda

func init() {
	// stdout and stderr are sent to AWS CloudWatch Logs
	log.Printf("Gin cold start")
	r := gin.Default()

	// Global middleware
	r.Use(gin.Logger())
	r.Use(gin.Recovery())

	config := configs.ServerConfig{
		PersonalizeConfig: configs.PersonalizeConfig{
			CampaignArn: helpers.GetEnv("PERSONALIZE_CAMPAIGN_ARN", ""),
			FilterArn: helpers.GetEnv("PERSONALIZE_FILTER_ARN", ""),
			FilterHistoriesSize: 100,
			FilterBlockSize: 100,
		},
		ExtUserServiceConfig: configs.ExtUserServiceConfig{
			Endpoint: helpers.GetEnv("SERVICE_USER_ENDPOINT", "https://q1efoi7143.execute-api.ap-southeast-1.amazonaws.com/dev/users"),
		},
	}

	router.Setup(r, config)

	ginLambda = ginadapter.New(r)
}

// Handler -
func Handler(ctx context.Context,req events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
 // If no name is provided in the HTTP request body, throw an error
	return ginLambda.ProxyWithContext(ctx, req)
}

func main() {
	lambda.Start(Handler)
}