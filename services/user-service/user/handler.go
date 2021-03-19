package user

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/user-service/api/pkg/helpers"
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
	followingTableName := helpers.GetEnv("DYNAMODB_TABLE_FOLLOWING", "Following")

	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatalf("failed to load SDK configuration, %v", err)
	}
	client := dynamodb.NewFromConfig(cfg)
	repository := NewDynamoDBRepository(client, DynamoDBConfig{
		HistoryTableName: historyTableName,
		BlockTableName: blockTableName,
		FollowingTableName: followingTableName,
		})
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
	
	// r.GET("/users/:id/following", handler.GetFollowingItemsByUserID)
	r.POST("/users/testcreatefollowing", handler.TestCreateFollowing)
	r.POST("/users/:id/following", handler.AddFollowingItemByUserID)
	r.PUT("/users/:id/following", handler.SaveFollowingItemByUserID)
	r.DELETE("/users/:id/following", handler.DeleteFollowingItemByItemID)
	r.GET("/users/:id/histories", handler.GetLatestHistoriesByUserID)
	r.GET("/users/:id/blocks", handler.GetLatestBlocksByUserID)
}

// GetLatestHistoriesByUserID -
func (h *UserHandler) GetLatestHistoriesByUserID(c *gin.Context) {
	userID := c.Param("id")
	limit := helpers.ParseStringToInt32(c.Query("limit"), 10) 

	data, err := h.usecase.GetLatestHistoriesByUserID(c.Request.Context(), userID, limit)

	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
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
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": data})
}

func (h *UserHandler) GetFollowingItemsByUserID(c *gin.Context) {
	userID := c.Param("id")

	fmt.Printf("query userID %v\n", userID)

	data, err := h.usecase.GetFollowingItemsByUserID(c.Request.Context(), userID)

	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": data})
}

func (h *UserHandler) DeleteFollowingItemByItemID(c *gin.Context) {
	userID := c.Param("id")
	itemID := c.Query("itemID")

	fmt.Printf("query userID %v\n", userID)

	err := h.usecase.DeleteFollowingItemByUserID(c.Request.Context(), userID, itemID)

	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": "OK"})
}

func (h *UserHandler) AddFollowingItemByUserID(c *gin.Context) {
	userID := c.Param("id")
	jsonData, _ := ioutil.ReadAll(c.Request.Body)
	followingItem := &FollowingItem{}
	json.Unmarshal(jsonData, followingItem)
	
	fmt.Println(string(jsonData))
	fmt.Println(followingItem)

	followingItem, err := h.usecase.AddFollowingItemByUserID(c.Request.Context(), userID, followingItem.Name, followingItem.Type)

	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": followingItem})
}

func (h *UserHandler) SaveFollowingItemByUserID(c *gin.Context) {
	userID := c.Param("id")
	jsonData, _ := ioutil.ReadAll(c.Request.Body)
	var body struct{FollowingItems []FollowingItem	`json:"followingItems"`}
	json.Unmarshal(jsonData, &body)

	err := h.usecase.SaveFollowingItems(c.Request.Context(), userID, body.FollowingItems)

	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": "OK"})
}

func (h *UserHandler) TestCreateFollowing(c *gin.Context) {
	userID := "164591f3-2a53-4c94-84eb-da692dca55ca"

	err := h.usecase.CreateFollowingForNewUser(c.Request.Context(), userID)

	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": "OK"})
}