package helper

import (
	"bytes"
	"encoding/json"

	"github.com/aws/aws-lambda-go/events"
)

// Response is of type APIGatewayProxyResponse since we're leveraging the
type Response events.APIGatewayProxyResponse

// Request is of type APIGatewayProxyResponse since we're leveraging the
type Request events.APIGatewayProxyRequest

// ResponseError is function that return with error message
func ResponseError(msg string, statusCode int) Response  {
	return Response{StatusCode: statusCode, Body: msg}
}

// ResponseSuccess is function that return with payload (JSON)
func ResponseSuccess(payload map[string]interface{}, statusCode int) (Response, error) {
	var buf bytes.Buffer
	
	body, err := json.Marshal(payload)

	if err != nil {
		return Response{}, err
	}

	json.HTMLEscape(&buf, body)

	return Response{
		StatusCode:      statusCode,
		IsBase64Encoded: false,
		Body:            buf.String(),
		Headers: map[string]string{
			"Content-Type":	"application/json",
		},
	}, nil
}