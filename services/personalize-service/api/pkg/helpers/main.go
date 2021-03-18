package helpers

import (
	"encoding/json"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/pkg/errors"
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

var myClient = &http.Client{Timeout: 10 * time.Second}

// GetHTTPJson -
func GetHTTPJson(url string, target interface{}) error {
    res, err := myClient.Get(url)
    if err != nil {
        return errors.Wrap(err,  "error HTTP request to")
    }
		
		defer res.Body.Close()

    return json.NewDecoder(res.Body).Decode(target)
}

// JoinSliceOfStruct -
func JoinSliceOfStruct(list []interface{},  cb func (e interface{}) string) []string {
	var strList []string

	for _, element := range(list) {
		strList = append(strList, cb(element))
	}

	return strList
}

// FormatSliceToPersonalizeFilter -
func FormatSliceToPersonalizeFilter(strList []string) string {
	if len(strList) == 0 {
		return "\"\""
	}

	// escape blackslash double quote => \"
	dq := "\""

	return dq + strings.Join(strList, dq + "," + dq) + dq
}