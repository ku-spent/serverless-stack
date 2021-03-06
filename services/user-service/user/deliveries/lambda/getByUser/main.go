package main

import (
	"context"
	"fmt"
	"log"
	"strconv"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/ku-spent/serverless-stack/personalize-service/api/internal/helper"
	"github.com/ku-spent/serverless-stack/personalize-service/api/user"
)

type handler struct {
	usecase user.Service
}


// Handler is our lambda handler invoked by the `lambda.Start` function call
func (h *handler) Handler(ctx context.Context, req helper.Request) (helper.Response, error) {
	userID := req.QueryStringParameters["id"]
	limit := req.QueryStringParameters["limit"]

	// parse to int32
	parsedLimit, _ := strconv.Atoi(limit)

	fmt.Printf("query userID %v, limit %v\n", userID, limit)

	
	data, err := h.usecase.GetLatestHistoriesByUserID(ctx, userID, int32(parsedLimit))
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
	usecase, err := user.Init()
	if err != nil {
		log.Panic(err)
	}

	h := handler{usecase: usecase}

	lambda.Start(h.Handler)
}