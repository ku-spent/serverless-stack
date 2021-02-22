package recommendation

import (
	"context"

	"github.com/pkg/errors"
)

type repository interface {
	GetByUser(ctx context.Context, userID string) (*Recommendation, error)
}

// Usecase of recommendation
type Usecase struct {
	Repository repository
}

// GetByUser is get recommendation for User by user id
func (u *Usecase) GetByUser(ctx context.Context, userID string) (*Recommendation, error) {
	recommendation, err := u.Repository.GetByUser(ctx, userID)
	if err != nil {
		return nil, errors.Wrap(err, "error get recommendation by user")
	}
	return recommendation, nil
}