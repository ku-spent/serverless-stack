package recommendation

import (
	"github.com/aws/aws-sdk-go-v2/service/personalizeruntime/types"
)

// Recommendation entitty
type Recommendation struct {
	ItemList []types.PredictedItem					`json:"itemList"`
	RecommendationID *string								`json:"RecommendationId"`
}

// Pagination entity
type Pagination struct {
	Limit int32
}
