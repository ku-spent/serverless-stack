package configs

// PersonalizeConfig -
type PersonalizeConfig struct {
	FilterArn	string
	CampaignArn string

	FilterHistoriesSize int32
	FilterBlockSize	int32
}

// ExtUserServiceConfig -
type ExtUserServiceConfig struct {
	Endpoint string
}

// ServerConfig -
type ServerConfig struct {
	PersonalizeConfig PersonalizeConfig
	ExtUserServiceConfig ExtUserServiceConfig
}