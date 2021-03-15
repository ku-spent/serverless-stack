package router

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/personalize-service/api/personalize"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/configs"
)

// Setup -
func Setup(r *gin.Engine, config configs.ServerConfig)  {
	personalize.NewPersonalizeHandler(r, config)

	r.GET("/heathcheck", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "Everything is OK 🚀"})
	})
}