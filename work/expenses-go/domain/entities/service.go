package entities

import (
	"github.com/google/uuid"
)

type Service struct {
	ID   uuid.UUID
	Name string
}

func NewService(name string) *Service {
	return &Service{
		ID:   uuid.New(),
		Name: name,
	}
}
