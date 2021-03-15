package main

import (
	"log"

	"github.com/gin-gonic/gin"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/configs"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/helpers"
	"github.com/ku-spent/serverless-stack/personalize-service/api/pkg/router"
)

func main() {
	r := gin.Default()

	// Global middleware
	r.Use(gin.Logger())
	r.Use(gin.Recovery())

	config := configs.ServerConfig{
		PersonalizeConfig: configs.PersonalizeConfig{
			CampaignArn: helpers.GetEnv("PERSONALIZE_CAMPAIGN_ARN", ""),
			FilterArn: helpers.GetEnv("PERSONALIZE_FILTER_ARN", ""),
			FilterHistoriesSize: 100,
			FilterBlockSize: 100,
		},
		ExtUserServiceConfig: configs.ExtUserServiceConfig{
			Endpoint: helpers.GetEnv("SERVICE_USER_ENDPOINT", "https://q1efoi7143.execute-api.ap-southeast-1.amazonaws.com/dev/users"),
		},
		ExtNewsServiceConfig: configs.ExtNewsServiceConfig{
			Endpoint: helpers.GetEnv("SERVICE_NEWS_ENDPOINT", "http://localhost:3000/dev/news"),
			// Endpoint: helpers.GetEnv("SERVICE_NEWS_ENDPOINT", "https://q1efoi7143.execute-api.ap-southeast-1.amazonaws.com/dev/news"),
		},
	}

	router.Setup(r, config)
  // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
	if err := r.Run(":8000"); err != nil { 
		log.Printf("error starting server %+v", err)
	}
}