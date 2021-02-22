package recommendation

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/personalizeruntime"
)

// Service -
type Service interface {
	GetByUser(ctx context.Context, userID string) (*Recommendation, error)
}

// Init sets up an instance of this domains
// usecase, pre-configured with the dependencies.
func Init() (Service, error) {
	// region := os.Getenv("AWS_REGION")
	campaignArn := os.Getenv("PERSONALIZE_CAMPAIGN_ARN")
	fmt.Println(campaignArn)
	filterArn := os.Getenv("PERSONALIZE_FILTER_ARN")

	// sess, err := session.NewSession(&aws.Config{Region: &region})
	// mySession := session.Must(session.NewSession())
	// client := personalizeruntime.New(aws.Config{Region: aws.ToString(&region)})
	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatalf("failed to load SDK configuration, %v", err)
	}
	client := personalizeruntime.NewFromConfig(cfg)
	repository := NewPersonalizeRepository(client, campaignArn, filterArn)
	usecase := &Usecase{Repository: repository}
	return usecase, nil
}