package main

import (
	"context"

	"github.com/aws/aws-lambda-go/events"
)

// Response is of type APIGatewayProxyResponse since we're leveraging the
type Response events.APIGatewayProxyResponse

// Request is of type APIGatewayProxyResponse since we're leveraging the
type Request events.APIGatewayProxyRequest

// Context is of type APIGatewayProxyResponse since we're leveraging the
type Context context.Context