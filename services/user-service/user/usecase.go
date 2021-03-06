package user

import (
	"context"

	"github.com/pkg/errors"
)

type repository interface {
	GetHistoriesByUserID(ctx context.Context, userID string, pagination Pagination) (*[]History, error)
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
	return histories, nil
}

// // GetLatestBlocksByUserID is function to get blocks by user id
// func (u *Usecase) GetLatestBlocksByUserID(ctx context.Context, userID string,  limit int) (*[]Block, error) {
// 	user, err := u.Repository.GetByUser(ctx, userID)
// 	if err != nil {
// 		return nil, errors.Wrap(err, "error get user by user")
// 	}
// 	return user, nil
// }