#!/usr/bin/env bash
docker compose up -d --build

echo "User setup"
curl -X POST http://localhost:8080/users/create -H "Content-Type: application/json" -d @./test_data/create_user.json
echo -e "\n"
curl -o ./test_scripts/script_output.json -X GET http://localhost:8080/users/user/ttangvz859@gmail.com
VID=$(jq -r '.id' ./test_scripts/script_output.json)
echo $VID
cat ./test_scripts/script_output.json
echo -e "\n"

echo "Convention setup"
jq --arg key "host_id" --arg value "$VID" '. += {($key): $value}' ./test_data/create_convention.json > ./test_data/temp.json && mv ./test_data/temp.json ./test_data/create_convention.json
cat ./test_data/create_convention.json
curl -o test_scripts/script_output.json -X POST http://localhost:8080/convention/create -H "Content-Type: application/json" -d @./test_data/create_convention.json
echo -e "\n"
CONV_ID=$(jq -r '.conv_id' ./test_scripts/script_output.json)

echo "Testing registration health check"
curl -X GET http://localhost:8080/registration/health
echo -e "\n"

echo "Testing register attendee"
curl -X POST http://localhost:8080/registration/register_user -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "attendee_id":"'"$VID"'"}'
echo -e "\n"

echo "Adding dummy registrations"
curl -X POST http://localhost:8080/registration/register_user -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "attendee_id":"dummy_attendee1"}'
echo -e "\n"
curl -X POST http://localhost:8080/registration/register_user -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "attendee_id":"dummy_attendee2"}'
echo -e "\n"

echo "Testing get attendees by conv_id"
curl -X POST http://localhost:8080/registration/get_attendees/$CONV_ID
echo -e "\n"

echo "Testing get conventions by user_id"
curl -X POST http://localhost:8080/registration/get_conventions/$VID
echo -e "\n"

echo "Testing unregister attendee"
curl -X DELETE http://localhost:8080/registration/unregister_user -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "attendee_id":"'"$VID"'"}'
echo -e "\n"

docker compose down -v
