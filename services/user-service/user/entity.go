package user

// User entitty
type User struct {
	// ItemList []types.PredictedItem					`json:"itemList"`
	// RecommendationID *string								`json:"RecommendationId"`
}

// History entity
type History struct {
	NewsID string
	NewsTitle string
	Status string
	CreatedAt string
	UpdateAt string
}

// Block entity
type Block struct {
	Name string
	Type string
	CreatedAt string
	UpdateAt string
}

// Pagination entity
type Pagination struct {
	Limit int32
}