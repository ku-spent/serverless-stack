package user

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/expression"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
)

// DynamoDBRepository -
type DynamoDBRepository struct {
	Client *dynamodb.Client
	Config DynamoDBConfig
}

// DynamoDBConfig - 
type DynamoDBConfig struct {
	HistoryTableName string
	BlockTableName string
}

// NewDynamoDBRepository is function to create Repository
func NewDynamoDBRepository(client *dynamodb.Client, dynamoDBConfig DynamoDBConfig) *DynamoDBRepository {
	return &DynamoDBRepository{
		Client: client,
		Config: dynamoDBConfig,
	}
}

// GetHistoriesByUserID -
func(r *DynamoDBRepository) GetHistoriesByUserID(ctx context.Context, userID string, pagination Pagination) (*[]History, error) {
	keyCond := expression.Key("userId").Equal(expression.Value(userID))
	filter1 := expression.Name("_deleted").NotEqual(expression.Value(true))
	expr, err := expression.NewBuilder().WithKeyCondition(keyCond).WithFilter(filter1).Build()

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
		TableName:									&r.Config.HistoryTableName,
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

// GetBlocksByUserID -
func(r *DynamoDBRepository) GetBlocksByUserID(ctx context.Context, userID string, pagination Pagination) (*[]Block, error) {
	keyCond := expression.Key("userId").Equal(expression.Value(userID))
	filter1 := expression.Name("_deleted").NotEqual(expression.Value(true))
	expr, err := expression.NewBuilder().WithKeyCondition(keyCond).WithFilter(filter1).Build()

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
		TableName:									&r.Config.BlockTableName,
	}
	fmt.Printf("params %+v\n", params)

	// Make the DynamoDB Query API call
	result, err := r.Client.Query(ctx, params)

	if err != nil {
		return nil, err
	}

	blocks := []Block{}

	err = attributevalue.UnmarshalListOfMaps(result.Items, &blocks)

	if err != nil {
		panic(fmt.Sprintf("Failed to unmarshal Dynamodb Scan Items, %v", err))
	}

	return &blocks, nil
}
