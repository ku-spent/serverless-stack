package user

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

// Service -
type Service interface {
	GetLatestHistoriesByUserID(ctx context.Context, userID string, limit int32) (*[]History, error)
	// GetLatestBlocksByUserID(ctx context.Context, userID string, limit int) (*[]Block, error)
}

// Init sets up an instance of this domains
// usecase, pre-configured with the dependencies.
func Init() (Service, error) {
	// region := os.Getenv("AWS_REGION")
	tableName := os.Getenv("TABLE_HISTORY")
	if tableName == "" {
		tableName = "History-rqchhvrcpvhcro3m3jspr63gmi-dev"
	}

	// sess, err := session.NewSession(&aws.Config{Region: &region})
	// mySession := session.Must(session.NewSession())
	// client := personalizeruntime.New(aws.Config{Region: aws.ToString(&region)})
	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatalf("failed to load SDK configuration, %v", err)
	}
	client := dynamodb.NewFromConfig(cfg)
	fmt.Println(tableName)
	repository := NewRepository(client, tableName)
	usecase := &Usecase{Repository: repository}
	return usecase, nil
}