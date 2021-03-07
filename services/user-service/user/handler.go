package user

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"strconv"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/helpers"
)

// UserHandler -
type UserHandler struct {
	usecase Usecase 
}

// Init pre-configured with the dependencies.
func Init() (Usecase, error) {
	// region := os.Getenv("AWS_REGION")
	historyTableName := helpers.GetEnv("DYNAMODB_TABLE_HISTORY", "History-rqchhvrcpvhcro3m3jspr63gmi-dev")
	blockTableName := helpers.GetEnv("DYNAMODB_TABLE_BLOCK", "Block-rqchhvrcpvhcro3m3jspr63gmi-dev")

	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatalf("failed to load SDK configuration, %v", err)
	}
	client := dynamodb.NewFromConfig(cfg)
	repository := NewDynamoDBRepository(client, DynamoDBConfig{HistoryTableName: historyTableName, BlockTableName: blockTableName})
	usecase := Usecase{Repository: repository}
	return usecase, nil
}

// NewUserHandler -
func NewUserHandler(r *gin.Engine) {
	u, err := Init()

	if err != nil {
		log.Panic(err)
	}

	handler := &UserHandler{
		usecase: u,
	}
	
	r.GET("/users/:id/histories", handler.GetLatestHistoriesByUserID)
	r.GET("/users/:id/blocks", handler.GetLatestBlocksByUserID)
}

// GetLatestHistoriesByUserID -
func (h *UserHandler) GetLatestHistoriesByUserID(c *gin.Context) {
	userID := c.Param("id")
	limit := c.Query("limit")

	// parse to int32
	parsedLimit, err := strconv.Atoi(limit)
	if err != nil {
		parsedLimit = 10
	}

	fmt.Printf("query userID %v, limit %v\n", userID, limit)

	data, err := h.usecase.GetLatestHistoriesByUserID(c.Request.Context(), userID, int32(parsedLimit))

	if err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": data})
}

// GetLatestBlocksByUserID -
func (h *UserHandler) GetLatestBlocksByUserID(c *gin.Context) {
	userID := c.Param("id")
	limit := c.Query("limit")

	// parse to int32
	parsedLimit, err := strconv.Atoi(limit)
	if err != nil {
		parsedLimit = 10
	}

	fmt.Printf("query userID %v, limit %v\n", userID, limit)

	data, err := h.usecase.GetLatestBlocksByUserID(c.Request.Context(), userID, int32(parsedLimit))

	if err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": data})
}