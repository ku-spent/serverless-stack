package personalize

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/service/personalizeruntime"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/helpers"
)

// PersonalizeRepository -
type PersonalizeRepository struct {
	Client *personalizeruntime.Client
	CampaignArn string
	FilterArn string
}

// PersonalizeFilter -
type PersonalizeFilter struct {
	Tags []string
	Sources []string
	Categories []string
}

// NewPersonalizeRepository is function to create PersonalizeRepository
func NewPersonalizeRepository(client *personalizeruntime.Client, campaignArn string, filterArn string) *PersonalizeRepository {
	return &PersonalizeRepository{
		Client: client,
		CampaignArn: campaignArn,
		FilterArn: filterArn,
	}
}

// GetRecommendationByUser personalize recommendation by userID
func(r *PersonalizeRepository) GetRecommendationByUser(ctx context.Context, userID string, personalizeFilter PersonalizeFilter, pagination Pagination) (*Recommendation, error) {
	filterValues := map[string]string{
		"tags": helpers.FormatSliceToPersonalizeFilter(personalizeFilter.Tags),
		"sources": helpers.FormatSliceToPersonalizeFilter(personalizeFilter.Sources),
		"categories": helpers.FormatSliceToPersonalizeFilter(personalizeFilter.Categories),
	}

	input := &personalizeruntime.GetRecommendationsInput{
		UserId: &userID,
		CampaignArn: &r.CampaignArn,
		FilterArn: &r.FilterArn,
		FilterValues: filterValues,
		NumResults: pagination.Limit,
	}
	fmt.Printf("%+v\n", input)

	output, err := r.Client.GetRecommendations(ctx, input)
	
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