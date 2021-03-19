package user

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/expression"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb/types"
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
	FollowingTableName string
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

// SaveFollowing -
func (r *DynamoDBRepository) SaveFollowing(ctx context.Context, userID string, followingItems []FollowingItem) error {
	following := Following{UserID: userID, Items: followingItems}
	av, err := attributevalue.MarshalMap(following)

	fmt.Println(av)

	if err != nil {
		return err
	}

	params := &dynamodb.PutItemInput{TableName: &r.Config.FollowingTableName, Item: av}
	_, err = r.Client.PutItem(ctx, params)

	if err != nil {
		return err
	}

	return nil
}

// AddFollowingItem -
func (r *DynamoDBRepository) AddFollowingItem(ctx context.Context, userID string, followingItem FollowingItem) error {
	av, err := attributevalue.MarshalMap(followingItem)
	newItem := &types.AttributeValueMemberM{Value: av}
	
	// update := expression.Set(
	// 	expression.Name("followingItems"), 
	// 	expression.Name("followingItems").ListAppend(expression.Value([]FollowingItem{followingItem})),
	// 	// expression.Name("followingItems").ListAppend(expression.Value(av)),
	// 	// IfNotExists(expression.Name("followingItems"), expression.Value(av)),
	// )

	// expr, err := expression.NewBuilder().WithUpdate(update).Build()
	
	params := &dynamodb.UpdateItemInput{
		TableName:	&r.Config.FollowingTableName,
		Key:	map[string]types.AttributeValue{
			"userID": &types.AttributeValueMemberS{Value: userID},
		},
		// ExpressionAttributeNames: expr.Names(),
		// ExpressionAttributeValues: expr.Values(),
		// UpdateExpression: expr.Update(),
		ExpressionAttributeValues: map[string]types.AttributeValue{
			":item": &types.AttributeValueMemberL{Value: []types.AttributeValue{newItem}},
			":empty_list": &types.AttributeValueMemberL{Value: []types.AttributeValue{}},
		},
		UpdateExpression: aws.String(fmt.Sprintf("SET followingItems = list_append(:item, if_not_exists(followingItems, :empty_list))")),
	}

	// Make the DynamoDB Query API call
	_, err = r.Client.UpdateItem(ctx, params)

	if err != nil {
		return err
	}

	return nil
}

// GetFollowingByUserID -
func (r *DynamoDBRepository) GetFollowingByUserID(ctx context.Context, userID string) (*Following, error) {
	// Build the query input parameters
	params := &dynamodb.GetItemInput{
		Key:	map[string]types.AttributeValue{
			"userID": &types.AttributeValueMemberS{Value: userID},
		},
		TableName:	&r.Config.FollowingTableName,
	}
	fmt.Printf("params %+v\n", params)

	// Make the DynamoDB Query API call
	result, err := r.Client.GetItem(ctx, params)

	if err != nil {
		return nil, err
	}

	following := Following{}

	err = attributevalue.UnmarshalMap(result.Item, &following)

	if err != nil {
		panic(fmt.Sprintf("Failed to unmarshal Dynamodb Scan Items, %v", err))
	}

	return &following, nil
}

func (r *DynamoDBRepository) DeleteFollowingItemByUserID(ctx context.Context, userID string, itemID string) (error) {
	following, err := r.GetFollowingByUserID(ctx, userID)

	idxToRemove := -1
	// nameToRemove := ""

	for i, item := range following.Items {
		if item.ID == itemID {
			idxToRemove = i
			// nameToRemove = item.Name
		}
	}

	// not found
	if idxToRemove == -1 {
		return  nil
	}

	params := &dynamodb.UpdateItemInput{
		TableName:	&r.Config.FollowingTableName,
		Key:	map[string]types.AttributeValue{
			"userID": &types.AttributeValueMemberS{Value: userID},
		},
		UpdateExpression: aws.String(fmt.Sprintf("REMOVE followingItems[%d]", idxToRemove)),
	}

	// Make the DynamoDB Query API call
	_, err = r.Client.UpdateItem(ctx, params)

	if err != nil {
		return err
	}

	return nil
}
