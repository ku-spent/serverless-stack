package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/ku-spent/serverless-stack/personalize-service/api/internal/helper"
	"github.com/ku-spent/serverless-stack/personalize-service/api/recommendation"
)

type handler struct {
	usecase recommendation.Service
}


// Handler is our lambda handler invoked by the `lambda.Start` function call
func (h *handler) Handler(ctx context.Context, req helper.Request) (helper.Response, error) {
	userID := req.QueryStringParameters["id"]
	fmt.Printf("query userID %v\n", userID)
	data, err := h.usecase.GetByUser(ctx, userID)
	if err != nil {
		return helper.ResponseError(err.Error(), 400), err
	}

	resp, err := helper.ResponseSuccess(map[string]interface{}{
		"message": "Go Serverless v1.0! Your function executed successfully!",
		"data": data,
	}, 200)

	return resp, nil
}

func main() {
	usecase, err := recommendation.Init()
	if err != nil {
		log.Panic(err)
	}

	h := handler{usecase: usecase}

	lambda.Start(h.Handler)
}