package helpers

import (
	"os"
	"strconv"
)

// GetEnv is function to get environment variable with default value
func GetEnv(key string, defaultValue string) string {
	val := os.Getenv(key)
	
	if val == "" {
		val = defaultValue
	}

	return val
}

// ParseStringToInt32 is function to parse string to int32 with default value
func ParseStringToInt32(val string, defaultValue int32) int32 {
	parsedVal, err := strconv.Atoi(val)
	if err != nil {
		return defaultValue
	}
	return int32(parsedVal)
}