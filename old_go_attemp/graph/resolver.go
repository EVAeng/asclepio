package graph

import (
	"github.com/EVAeng/asclepio/graph/model"
)

//go:generate go run github.com/99designs/gqlgen

type Resolver struct{
	doctors []*model.Doctor
}
