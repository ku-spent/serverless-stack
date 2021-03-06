package recommendation

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/service/personalizeruntime"
)

// PersonalizeRepository -
type PersonalizeRepository struct {
	Client *personalizeruntime.Client
	CampaignArn string
	FilterArn string
}

// NewPersonalizeRepository is function to create PersonalizeRepository
func NewPersonalizeRepository(client *personalizeruntime.Client, campaignArn string, filterArn string) *PersonalizeRepository {
	return &PersonalizeRepository{
		Client: client,
		CampaignArn: campaignArn,
		FilterArn: filterArn,
	}
}

// GetByUser personalize recommendation by userID
func(r *PersonalizeRepository) GetByUser(ctx context.Context, userID string) (*Recommendation, error) {
	input := &personalizeruntime.GetRecommendationsInput{
		UserId: &userID,
		CampaignArn: &r.CampaignArn,
		// FilterArn: &r.FilterArn,
		NumResults: 20,
	}
	fmt.Printf("%+v\n", input)

	output, err := r.Client.GetRecommendations(ctx, input)
	fmt.Printf("output %+v\n", output)
	fmt.Printf("err %+v\n", err)
	if err != nil {
		return nil, err
	}

	recommendation := &Recommendation{
		RecommendationID: output.RecommendationId,
		ItemList: output.ItemList,
	}
	fmt.Printf("%+v\n", recommendation)

	return recommendation, nil
}