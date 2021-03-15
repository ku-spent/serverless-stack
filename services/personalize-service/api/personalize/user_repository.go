package personalize

import (
	"context"
	"fmt"

	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/helpers"
)

// UserRepository -
type UserRepository struct {
	UserEndpoint string
}

// NewUserRepository is function to create UserRepository
func NewUserRepository(userEndpoint string) *UserRepository {
	return &UserRepository{
		UserEndpoint: userEndpoint,
	}
}

// GetHistoriesByUserID -
func (r *UserRepository) GetHistoriesByUserID(ctx context.Context, userID string, pagination Pagination) (*[]History, error){
	var resp struct{Data []History	`json:"data"`}
	endpoint := fmt.Sprintf("/%s/histories?limit=%d", userID, pagination.Size)
	err := helpers.GetHTTPJson(r.UserEndpoint + endpoint, &resp)

	if err != nil {
		return nil, err
	}

	return &resp.Data, nil
}

// GetBlocksByUserID -
func (r *UserRepository) 	GetBlocksByUserID(ctx context.Context, userID string, pagination Pagination) (*[]Block, error){
	var resp struct{Data []Block	`json:"data"`}
	endpoint := fmt.Sprintf("/%s/blocks?limit=%d", userID, pagination.Size)
	err := helpers.GetHTTPJson(r.UserEndpoint + endpoint, &resp)

	if err != nil {
		return nil, err
	}

	return &resp.Data, nil
}