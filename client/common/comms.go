package common

import (
	"bufio"
	"errors"
	"net"
	"strconv"
	"strings"
)

const TYPE_SEPARATOR = "|"
const ACK_FIELD_SEPARATOR = ","

type Type int

const (
	ACK Type = iota
	BET
)

func splitAckPacket(packet string) (string, string, error) {
	splitPacket := strings.Split(packet, TYPE_SEPARATOR)

	pType, err := strconv.Atoi(splitPacket[0])
	if err != nil {
		return "", "", err
	}

	if pType != int(ACK) {
		return "", "", errors.New("Message is not ACK")
	}

	ackRaw := splitPacket[1]
	ackArr := strings.Split(ackRaw, ACK_FIELD_SEPARATOR)

	return ackArr[0], ackArr[1], nil
}

func WriteBet(conn net.Conn, bet Bet) error {
	writer := bufio.NewWriter(conn)
	packet := bet.TurnToString()

	_, err := writer.WriteString(packet)
	if err != nil {
		log.Errorf("action: send_message | result: fail | error: %v",
			err,
		)
		return err
	}
	writer.Flush()

	return nil
}

func ReadACK(conn net.Conn, client_id string) (string, string, error) {
	packet, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		return "", "", err
	}

	dni, numero, err := splitAckPacket(packet)
	if err != nil {
		log.Errorf("action: apuesta_enviada | result: fail | client_id: %v}",
			client_id,
		)
		return "", "", err
	}

	conn.Close()

	return dni, numero, nil
}
