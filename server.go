package main

import (
	"os"

	"github.com/EVAeng/asclepio/http"
	"github.com/gin-gonic/gin"
)

const defaultPort = ":8080"

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	server := gin.Default()
	
	server.GET("/", http.PlaygroundHandler())
	server.POST("/query", http.GraphQLHandler())

	server.Run(port)
}
