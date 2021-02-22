package main

import (
	"context"
	"fmt"
	"log"

	"github.com/ku-spent/serverless-stack/personalize-service/api/recommendation"
)

type handler struct {
	usecase recommendation.Service
}

// Handler is our lambda handler invoked by the `lambda.Start` function call
func (h *handler) Handler(ctx context.Context) {
	userID := "2"
	fmt.Printf("query userID %v\n", userID)
	data, err := h.usecase.GetByUser(ctx, userID)
	fmt.Printf("%+v\n", data)
	fmt.Printf("%+v\n", err)
}

func main() {
	usecase, err := recommendation.Init()
	if err != nil {
		log.Panic(err)
	}

	
	h := handler{usecase: usecase}
	ctx := context.Background()
	h.Handler(ctx)
}