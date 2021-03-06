package user

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/expression"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

// Repository -
type Repository struct {
	Client *dynamodb.Client
	TableName string
}

// NewRepository is function to create Repository
func NewRepository(client *dynamodb.Client, tableName string) *Repository {
	return &Repository{
		Client: client,
		TableName: tableName,
	}
}

// func(r *Repository)  GetLatestHistoriesByUserID(ctx context.Context, userID string, limit int) (*[]History, error)
// func(r *Repository)  	GetLatestBlocksByUserID(ctx context.Context, userID string, limit int) (*[]Block, error)


// GetHistoriesByUserID -
func(r *Repository) GetHistoriesByUserID(ctx context.Context, userID string, pagination Pagination) (*[]History, error) {
	filt1 := expression.Key("userId").Equal(expression.Value(userID))
	expr, err := expression.NewBuilder().WithKeyCondition(filt1).Build()

	isAsc := false

	index := "byUser"
	// Build the query input parameters
	params := &dynamodb.QueryInput{
		ScanIndexForward: &isAsc,
		IndexName: &index,
		ExpressionAttributeNames:  	expr.Names(),
		ExpressionAttributeValues: 	expr.Values(),
		KeyConditionExpression: 		expr.KeyCondition(),
		ProjectionExpression:      	expr.Projection(),
		FilterExpression: 					expr.Filter(),
		Limit: 											&pagination.Limit,
		TableName:									&r.TableName,
	}
	fmt.Printf("params %+v\n", params)

	// Make the DynamoDB Query API call
	result, err := r.Client.Query(ctx, params)

	if err != nil {
		return nil, err
	}

	histories := []History{}

	err = attributevalue.UnmarshalListOfMaps(result.Items, &histories)

	if err != nil {
		panic(fmt.Sprintf("Failed to unmarshal Dynamodb Scan Items, %v", err))
	}

	return &histories, nil
}