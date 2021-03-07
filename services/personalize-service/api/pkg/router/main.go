package router

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/personalize-service/api/recommendation"
)

// Setup -
func Setup(r *gin.Engine)  {
	recommendation.NewPersonalizeHandler(r)

	r.GET("/heathcheck", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "Everything is OK 🚀"})
	})
}