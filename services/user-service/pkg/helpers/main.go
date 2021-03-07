package helpers

import "os"

// GetEnv is function to get environment variable with default value
func GetEnv(key string, defaultValue string) string {
	val := os.Getenv(key)
	
	if val == "" {
		val = defaultValue
	}

	return val
}