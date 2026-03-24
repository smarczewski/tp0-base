#!/bin/bash
MSG="hello world"
IP="server"
PORT=12345
NETWORK="tp0_testing_net"

RESPONSE=$(docker run --network=$NETWORK -it --rm busybox sh -c "echo '$MSG' | nc $IP $PORT")

if [ "$RESPONSE" = "$MSG" ]; then
    echo "action: test_echo_server | result: success"
else
    echo "action: test_echo_server | result: fail"
fi