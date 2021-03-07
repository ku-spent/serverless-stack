package user

import (
	"context"
	"fmt"

	"github.com/pkg/errors"
)

type repository interface {
	GetHistoriesByUserID(ctx context.Context, userID string, pagination Pagination) (*[]History, error)
	GetBlocksByUserID(ctx context.Context, userID string, pagination Pagination) (*[]Block, error)
}

// Usecase of user
type Usecase struct {
	Repository repository
}

// GetLatestHistoriesByUserID is function to get histories by user id
func (u *Usecase) GetLatestHistoriesByUserID(ctx context.Context, userID string, limit int32) (*[]History, error) {
	histories, err := u.Repository.GetHistoriesByUserID(ctx, userID, Pagination{Limit: limit})
	if err != nil {
		return nil, errors.Wrap(err, "error get histories by user")
	}
	fmt.Printf("histories length %v\n", len(*histories))
	return histories, nil
}

// GetLatestBlocksByUserID is function to get blocks by user id
func (u *Usecase) GetLatestBlocksByUserID(ctx context.Context, userID string, limit int32) (*[]Block, error) {
	blocks, err := u.Repository.GetBlocksByUserID(ctx, userID, Pagination{Limit: limit})
	if err != nil {
		return nil, errors.Wrap(err, "error get blocks by user")
	}
	fmt.Printf("blocks length %v\n", len(*blocks))
	return blocks, nil
}