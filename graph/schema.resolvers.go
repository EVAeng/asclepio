package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"math/rand"
	"strconv"

	"github.com/EVAeng/asclepio/db"
	"github.com/EVAeng/asclepio/graph/generated"
	"github.com/EVAeng/asclepio/graph/model"
)

var doctorsCollection db.DoctorsCollection = db.New()

func (r *mutationResolver) CreateDoctor(ctx context.Context, input model.NewDoctor) (*model.Doctor, error) {
	doctor := &model.Doctor{
		ID:          strconv.Itoa(rand.Int()),
		Name:        input.Name,
		Price:       input.Price,
		Specialties: input.Specialties,
	}

	doctorsCollection.Save(doctor)

	return doctor, nil
}

func (r *queryResolver) Doctors(ctx context.Context) ([]*model.Doctor, error) {
	return doctorsCollection.FindAll(), nil
}

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
