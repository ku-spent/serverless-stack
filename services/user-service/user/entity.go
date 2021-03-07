package user

// User entitty
type User struct {
	// ItemList []types.PredictedItem					`json:"itemList"`
	// RecommendationID *string								`json:"RecommendationId"`
}

// History entity
type History struct {
	NewsID string						`json:"newsId"`
	NewsTitle string				`json:"newsTitle"`
	Status string						`json:"status"`
	CreatedAt string				`json:"createdAt"`
	UpdateAt string					`json:"updatedAt"`
}

// Block entity
type Block struct {
	Name string							`json:"name"`
	Type string							`json:"type"`
	CreatedAt string				`json:"createdAt"`
	UpdateAt string					`json:"updatedAt"`
}

// Pagination entity
type Pagination struct {
	Limit int32
}
