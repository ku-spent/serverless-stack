package router

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/personalize-service/api/user"
)

// Setup -
func Setup(r *gin.Engine)  {
	user.NewUserHandler(r)

	r.GET("/heathcheck", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "Everything is OK 🚀"})
	})
}