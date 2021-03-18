package personalize

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/service/personalizeruntime"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/configs"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/helpers"
	"github.com/thoas/go-funk"
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
	
	categories, _ := funk.DifferenceString(configs.AllNewsCategories, personalizeFilter.Categories)

	filterValues := map[string]string{
		"categories": helpers.FormatSliceToPersonalizeFilter(categories),
		"blockTags": helpers.FormatSliceToPersonalizeFilter(personalizeFilter.Tags),
		"blockSources": helpers.FormatSliceToPersonalizeFilter(personalizeFilter.Sources),
	}

	input := &personalizeruntime.GetRecommendationsInput{
		UserId: &userID,
		CampaignArn: &r.CampaignArn,
		FilterArn: &r.FilterArn,
		FilterValues: filterValues,
		NumResults: pagination.Size,
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

