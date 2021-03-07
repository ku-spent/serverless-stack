package recommendation

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/personalizeruntime"
	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/helpers"
)

// PersonalizeHandler -
type PersonalizeHandler struct {
	// GetByUser(ctx context.Context, userID string) (*Recommendation, error)
	usecase Usecase
}

// Init sets up an instance of this domains
// usecase, pre-configured with the dependencies.
func Init() (Usecase, error) {
	campaignArn := os.Getenv("PERSONALIZE_CAMPAIGN_ARN")
	filterArn := os.Getenv("PERSONALIZE_FILTER_ARN")

	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatalf("failed to load SDK configuration, %v", err)
	}
	client := personalizeruntime.NewFromConfig(cfg)
	repository := NewPersonalizeRepository(client, campaignArn, filterArn)
	usecase := Usecase{Repository: repository}
	return usecase, nil
}

// NewPersonalizeHandler -
func NewPersonalizeHandler(r *gin.Engine) {
	u, err := Init()

	if err != nil {
		log.Panic(err)
	}

	handler := &PersonalizeHandler{
		usecase: u,
	}
	
	r.GET("/recommendations", handler.GetByUser)
}

// GetByUser -
func (h *PersonalizeHandler) GetByUser(c *gin.Context) {
	userID := c.Query("id")
	limit := helpers.ParseStringToInt32(c.Query("limit"), 20) 


	fmt.Printf("query userID %v, limit %v\n", userID, limit)

	data, err := h.usecase.GetByUser(c.Request.Context(), userID, limit)

	if err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": data})
}