package db

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/EVAeng/asclepio/graph/model"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type DoctorsCollection interface {
	Save(doctor *model.Doctor)
	FindAll() []*model.Doctor
}

type Database struct {
	client *mongo.Client
}
 
const (
	DATABASE = "asclepio"
	COLLECTION = "doctors"
)

func New() DoctorsCollection  {

	MONGODB := "mongodb://localhost:27017"

	clientOptions := options.Client().ApplyURI(MONGODB)

	clientOptions = clientOptions.SetMaxPoolSize(50)

	ctx, _ := context.WithTimeout(context.Background(), 30*time.Second)

	dbClient, err := mongo.Connect(ctx, clientOptions)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to MongoDB")
	
	return &Database{
		client: dbClient,
	}
}

func (db *Database) Save(doctor *model.Doctor) {
	collection := db.client.Database(DATABASE).Collection(COLLECTION)
	_, err := collection.InsertOne(context.TODO(), doctor)

	if err != nil {
		log.Fatal(err)
	}
	
}

func (db *Database) FindAll() []*model.Doctor {
	collection := db.client.Database(DATABASE).Collection(COLLECTION)
	cursor, err := collection.Find(context.TODO(), bson.D{})

	if err != nil {
		log.Fatal(err)
	}

	defer cursor.Close(context.TODO())

	var result []*model.Doctor

	for cursor.Next(context.TODO()) {
		var doctorTemp *model.Doctor

		err := cursor.Decode(&doctorTemp)

		if err != nil {
			log.Fatal(err)
		}

		result = append(result, doctorTemp)
	}
	return result
}
