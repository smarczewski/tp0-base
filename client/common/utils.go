package common

import "fmt"

type Bet struct {
	Agency    string
	FirstName string
	LastName  string
	Document  string
	Birthdate string
	Number    string
}

func (bet Bet) TurnToString() string {
	betStr := fmt.Sprintf("%d|%s,%s,%s,%s,%s,%s\n", BET, bet.Agency, bet.FirstName, bet.LastName, bet.Document, bet.Birthdate, bet.Number)

	return betStr
}
