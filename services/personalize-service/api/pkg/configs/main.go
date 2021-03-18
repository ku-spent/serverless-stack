package configs

// PersonalizeConfig -
type PersonalizeConfig struct {
	FilterArn	string
	CampaignArn string

	FilterBlockSize	int32
	FilterHistoriesSize int32
}

// ExtUserServiceConfig -
type ExtUserServiceConfig struct {
	Endpoint string
}

type ExtNewsServiceConfig struct {
	Endpoint string
}

// ServerConfig -
type ServerConfig struct {
	PersonalizeConfig PersonalizeConfig
	ExtUserServiceConfig ExtUserServiceConfig
	ExtNewsServiceConfig ExtNewsServiceConfig
}

var AllNewsCategories = []string{
	"การเมือง",
	"เศรษฐกิจ",
	"ต่างประเทศ",
	"อาชญากรรม",
	"กีฬา",
	"ในประเทศ",
	"บันเทิง",
	"ไลฟ์สไตล์",
	"สิ่งแวดล้อม",
	"เทคโนโลยี",
	"สังคม",
	"คุณภาพชีวิต",
	"การศึกษา",
	"ภาพยนตร์",
	"เพลง",
	"ai",
	"data-science",
	"web-development",
	"big-data",
	"marketing",
	"deep-learning",
	"machine-learning",
	"data-science",
	"cybersecurity",
	"blockchain",
	"bitcoin",
	"startups",
	"programming",
}