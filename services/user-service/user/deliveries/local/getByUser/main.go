package main

import (
	"context"
	"fmt"
	"log"

	"github.com/ku-spent/serverless-stack/personalize-service/api/user"
)

type handler struct {
	usecase user.Service
}

// Handler is our lambda handler invoked by the `lambda.Start` function call
func (h *handler) Handler(ctx context.Context) {
	userID := "164591f3-2a53-4c94-84eb-da692dca55ca"
	fmt.Printf("query userID %v\n", userID)
	data, err := h.usecase.GetLatestHistoriesByUserID(ctx, userID, 1)
	fmt.Printf("%+v\n", data)
	fmt.Printf("%+v\n", err)
}

func main() {
	usecase, err := user.Init()
	if err != nil {
		log.Panic(err)
	}

	
	h := handler{usecase: usecase}
	ctx := context.Background()
	h.Handler(ctx)
}