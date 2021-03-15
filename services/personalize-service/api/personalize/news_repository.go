package personalize

import (
	"context"
	"fmt"

	"github.com/google/go-querystring/query"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/helpers"
)

// UserRepository -
type NewsRepository struct {
	NewsEndpoint string
}

// NewUserRepository is function to create UserRepository
func NewNewsRepository(newsEndpoint string) *NewsRepository {
	return &NewsRepository{
		NewsEndpoint: newsEndpoint,
	}
}

type NewsQuery struct {
	From int32											`url:"from"`
	Size int32											`url:"size"`
	FilterTags []string							`url:"filterTags"`
	FilterSources []string					`url:"filterSources"`
	FilterCategories []string				`url:"filterCategories"`
}
// GetRecommendationByUser personalize recommendation by userID
func(r *NewsRepository) GetLatestNews(ctx context.Context, newsQuery NewsQuery) (*map[string]interface{}, error) {
	var resp map[string]interface{}
	q, err := query.Values(newsQuery)
	if err != nil {
		return nil, err
	}

	fmt.Println(q)

	fmt.Println(q.Encode())

	endpoint := fmt.Sprintf("?%s", q.Encode())
	err = helpers.GetHTTPJson(r.NewsEndpoint + endpoint, &resp)

	if err != nil {
		return nil, err
	}

	return &resp, nil
}