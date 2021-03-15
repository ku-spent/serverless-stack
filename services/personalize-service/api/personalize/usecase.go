package personalize

import (
	"context"
	"fmt"

	"github.com/pkg/errors"
)

type personalizeRepository interface {
	GetRecommendationByUser(ctx context.Context, userID string, personalizeFilter PersonalizeFilter, pagination Pagination) (*Recommendation, error)
}

type userRepository interface {
	GetHistoriesByUserID(ctx context.Context, userID string, pagination Pagination) (*[]History, error)
	GetBlocksByUserID(ctx context.Context, userID string, pagination Pagination) (*[]Block, error)
}


type newsRepository interface {
	GetLatestNews(ctx context.Context, newsQuery NewsQuery) (*map[string]interface{}, error)
}

// Usecase of recommendation
type Usecase struct {
	PersonalizeRepository personalizeRepository
	UserRepository userRepository
	NewsRepository newsRepository
}

// GetRecommendationByUser is get recommendation for User by user id
func (u *Usecase) GetRecommendationByUser(ctx context.Context, userID string, size int32) (*Recommendation, error) {
	// _, err := u.UserRepository.GetHistoriesByUserID(ctx, userID,  Pagination{Size: 100})
	// if err != nil {
	// 	return nil, errors.Wrap(err, "error get recommendation by user")
	// }


	blocks, err := u.UserRepository.GetBlocksByUserID(ctx, userID,  Pagination{Size: 100})
	if err != nil {
		fmt.Println(err)
		return nil, errors.Wrap(err, "error get recommendation by user")
	}

	blockTags := []string{}
	blockSources := []string{}
	blockCategories := []string{}

	for _, block := range(*blocks) {
		switch block.Type {
		case "TAG":
			blockTags = append(blockTags, block.Name)
		case "SOURCE":
			blockSources = append(blockSources, block.Name)
		case "CATEGORY":
			blockCategories = append(blockCategories, block.Name)
		default:
		}
	}

	// fmt.Println(blocks)

	personalizeFilter := PersonalizeFilter{
		Tags: blockTags,
		Sources: blockSources,
		Categories: blockCategories,
	}

	recommendation, err := u.PersonalizeRepository.GetRecommendationByUser(ctx, userID, personalizeFilter, Pagination{Size: 30})
	if err != nil {
		return nil, errors.Wrap(err, "error get recommendation by user")
	}
	return recommendation, nil
}

// GetLatestNewsByUser -
func (u *Usecase) GetLatestNewsByUser(ctx context.Context, userID string, from int32, size int32) (*map[string]interface{}, error) {
	// _, err := u.UserRepository.GetHistoriesByUserID(ctx, userID,  Pagination{Size: 100})
	// if err != nil {
	// 	return nil, errors.Wrap(err, "error get recommendation by user")
	// }

	blocks, err := u.UserRepository.GetBlocksByUserID(ctx, userID,  Pagination{Size: 100})
	if err != nil {
		fmt.Println(err)
		return nil, errors.Wrap(err, "error get recommendation by user")
	}

	blockTags := []string{}
	blockSources := []string{}
	blockCategories := []string{}

	for _, block := range(*blocks) {
		switch block.Type {
		case "TAG":
			blockTags = append(blockTags, block.Name)
		case "SOURCE":
			blockSources = append(blockSources, block.Name)
		case "CATEGORY":
			blockCategories = append(blockCategories, block.Name)
		default:
		}
	}

	data, err := u.NewsRepository.GetLatestNews(ctx, NewsQuery{
		From: from,
		Size: size,
		FilterTags: blockTags,
		FilterSources: blockSources,
		FilterCategories: blockCategories,
	})

	if err != nil {
		return nil, errors.Wrap(err, "error get Latest news by user")
	}
	return data, nil
}
