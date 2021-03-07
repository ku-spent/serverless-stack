package main

import (
	"log"

	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/router"
)

func main() {
	r := gin.Default()

	// Global middleware
	r.Use(gin.Logger())
	r.Use(gin.Recovery())

	router.Setup(r)
  // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
	if err := r.Run(":3000"); err != nil { 
		log.Printf("error starting server %+v", err)
	}
}