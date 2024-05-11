package main

import (
	"encoding/json"
	"log"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

type body struct {
	Message string `json:"message"`
}

// Handler is the entry point for the AWS Lambda function.
// It takes an APIGatewayProxyRequest object which contains information about the incoming authorization request.
// It returns an APIGatewayProxyResponse object which contains the response to be returned by the API Gateway
func Handler(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	log.Println("hello from lambda", request.RequestContext.RequestID)
	b, _ := json.Marshal(body{Message: "hello world"})
	return events.APIGatewayProxyResponse{
		Body:       string(b),
		StatusCode: 200,
	}, nil
}


func main() {
	lambda.Start(Handler)
}
