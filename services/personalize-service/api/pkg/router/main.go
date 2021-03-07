package router

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/configs"
	"github.com/ku-spent/serverless-stack/personalize-service/api/recommendation"
)

// Setup -
func Setup(r *gin.Engine, config configs.ServerConfig)  {
	recommendation.NewPersonalizeHandler(r, config)

	r.GET("/heathcheck", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "Everything is OK 🚀"})
	})
}