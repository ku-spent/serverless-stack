package personalize

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/personalizeruntime"
	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/configs"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/helpers"
)

// PersonalizeHandler -
type PersonalizeHandler struct {
	usecase Usecase
}

// Init sets up an instance of this domains
// usecase, pre-configured with the dependencies.
func Init(c configs.ServerConfig) (Usecase, error) {
	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatalf("failed to load SDK configuration, %v", err)
	}
	client := personalizeruntime.NewFromConfig(cfg)
	personalizeRepository := NewPersonalizeRepository(client, c.PersonalizeConfig.CampaignArn, c.PersonalizeConfig.FilterArn)
	userRepository := NewUserRepository(c.ExtUserServiceConfig.Endpoint)
	newsRepository := NewNewsRepository(c.ExtNewsServiceConfig.Endpoint)
	usecase := Usecase{
		PersonalizeRepository: personalizeRepository,
		UserRepository: userRepository,
		NewsRepository: newsRepository,
	}
	return usecase, nil
}

// NewPersonalizeHandler -
func NewPersonalizeHandler(r *gin.Engine, config configs.ServerConfig) {
	u, err := Init(config)

	if err != nil {
		log.Panic(err)
	}

	handler := &PersonalizeHandler{
		usecase: u,
	}
	
	// r.GET("/test", handler.Test)
	basePath := "/personalize"
	r.GET(basePath + "/recommendations", handler.GetRecommendationByUser)
	r.GET(basePath + "/latest", handler.GetLatestNewsByUser)
}

// GetRecommendationByUser -
func (h *PersonalizeHandler) GetRecommendationByUser(c *gin.Context) {
	userID := c.Query("id")
	size := helpers.ParseStringToInt32(c.Query("size"), 20) 


	fmt.Printf("query userID %v, size %v\n", userID, size)

	data, err := h.usecase.GetRecommendationByUser(c.Request.Context(), userID, size)

	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": data})
}

// GetLatestNewsByUser -
func (h *PersonalizeHandler) GetLatestNewsByUser(c *gin.Context) {
	userID := c.Query("id")
	from := helpers.ParseStringToInt32(c.Query("from"), 0)
	size := helpers.ParseStringToInt32(c.Query("size"), 5)


	fmt.Printf("query userID %v, from: %v size: %v\n", userID, from, size)

	data, err := h.usecase.GetLatestNewsByUser(c.Request.Context(), userID, from, size)

	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}

	c.JSON(http.StatusOK, data)
}