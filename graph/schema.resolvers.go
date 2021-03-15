package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"fmt"
	"math/rand"

	"github.com/EVAeng/asclepio/graph/generated"
	"github.com/EVAeng/asclepio/graph/model"
)

func (r *mutationResolver) CreateDoctor(ctx context.Context, input model.NewDoctor) (*model.Doctor, error) {
	doctor := &model.Doctor{
		ID:          fmt.Sprintf("T%d", rand.Int()),
		Name:        input.Name,
		Price:       input.Price,
		Specialties: input.Specialties,
	}

	r.doctors = append(r.doctors, doctor)
	return doctor, nil
}

func (r *queryResolver) Doctors(ctx context.Context) ([]*model.Doctor, error) {
	return r.doctors, nil
}

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
