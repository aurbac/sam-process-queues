#!/bin/bash
echo $QUEUE_URL
echo "Container"
aws sqs send-message --queue-url $QUEUE_URL --message-body "Information about the largest city in Any Region." --delay-seconds 10 --message-attributes file://send-message.json