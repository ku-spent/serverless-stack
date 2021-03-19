package user

import (
	"context"
	"fmt"

	"github.com/google/uuid"
	"github.com/pkg/errors"
)

type repository interface {
	GetHistoriesByUserID(ctx context.Context, userID string, pagination Pagination) (*[]History, error)
	GetBlocksByUserID(ctx context.Context, userID string, pagination Pagination) (*[]Block, error)
	SaveFollowing(ctx context.Context, userID string, followingItems []FollowingItem) error
	GetFollowingByUserID(ctx context.Context, userID string) (*Following, error)
	AddFollowingItem(ctx context.Context, userID string, followingItem FollowingItem) error
	DeleteFollowingItemByUserID(ctx context.Context, userID string, itemID string) (error)
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

// CreateFollowingForNewUser -
func (u *Usecase) CreateFollowingForNewUser(ctx context.Context, userID string) (error) {
	followingItems := []FollowingItem{
		{
			ID: uuid.NewString(),
			Name: "Voice TV",
			Type: "SOURCE",
		},
		{
			ID: uuid.NewString(),
			Name: "มติชน",
			Type: "SOURCE",
		},
		{
			ID: uuid.NewString(),
			Name: "การเมือง",
			Type: "TAG",
		},
	}
	err := u.Repository.SaveFollowing(ctx, userID, followingItems)
	if err != nil {
		return errors.Wrap(err, "error create following for user")
	}
	return nil
}

// CreateFollowingForNewUser -
func (u *Usecase) SaveFollowingItems(ctx context.Context, userID string, followingItems []FollowingItem) (error) {
	err := u.Repository.SaveFollowing(ctx, userID, followingItems)
	if err != nil {
		return errors.Wrap(err, "error create following for user")
	}
	return nil
}

// GetFollowingItemsByUserID -
func (u *Usecase) GetFollowingItemsByUserID(ctx context.Context, userID string) (*[]FollowingItem, error) {
	following, err := u.Repository.GetFollowingByUserID(ctx, userID)

	if err != nil {
		return nil, errors.Wrap(err, "error get followingList by user")
	}

	fmt.Printf("blocks length %v\n", len(*&following.Items))
	return &following.Items, nil
}

// GetFollowingByUserID -
func (u *Usecase) AddFollowingItemByUserID(ctx context.Context, userID string, name string, ftype string) (*FollowingItem, error) {
	
	// check is exist
	following, err := u.Repository.GetFollowingByUserID(ctx, userID)

	isExist := false

	for _, item := range following.Items {
		if(item.Name == name && item.Type == ftype) {
			isExist = true
			break
		}
	}

	if isExist {
		return nil, nil
	}

	followingItem := FollowingItem{
		ID: uuid.NewString(),
		Name: name,
		Type: ftype,
	}

	err = u.Repository.AddFollowingItem(ctx, userID, followingItem)
	if err != nil {
		return nil, errors.Wrap(err, "error add followingItem by user")
	}
	// fmt.Printf("blocks length %v\n", len(*followingList))
	return &followingItem, nil
}

// DeleteFollowingItemByUserID -
func (u *Usecase) DeleteFollowingItemByUserID(ctx context.Context, userID string, itemID string) (error) {
	err := u.Repository.DeleteFollowingItemByUserID(ctx, userID, itemID)
	if err != nil {
		return errors.Wrap(err, "error delete followingItem by userID, itemID")
	}
	return nil
}