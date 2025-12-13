#!/usr/bin/env bash
docker compose up -d --build

echo "User setup"
curl -X POST http://localhost:8080/users/create -H "Content-Type: application/json" -d @./test_data/create_user.json
echo -e "\n"
curl -o ./test_scripts/script_output.json -X GET http://localhost:8080/users/user/ttangvz859@gmail.com
USER_ID=$(jq -r '.id' ./test_scripts/script_output.json)

jq --arg key "host_id" --arg value "$USER_ID" '. += {($key): $value}' ./test_data/create_convention.json > ./test_data/temp.json && mv ./test_data/temp.json ./test_data/create_convention.json
cat ./test_data/create_convention.json

echo "Convention Health Check"
curl -X GET http://localhost:8080/convention/health
echo -e "\n"

echo "Testing create convention"
curl -o test_scripts/script_output.json -X POST http://localhost:8080/convention/create -H "Content-Type: application/json" -d @./test_data/create_convention.json
echo -e "\n"

echo "Testing get all conventions"
echo "Adding two more conventions..."
curl -X POST http://localhost:8080/convention/create -H "Content-Type: application/json" -d @./test_data/dummy_convention.json
curl -X POST http://localhost:8080/convention/create -H "Content-Type: application/json" -d @./test_data/dummy_convention.json
echo -e "\n"
curl -X POST http://localhost:8080/convention/get -H "Content-Type: application/json" -d '{}'
echo -e "\n"

echo "Testing get conventions by host"
curl -X POST http://localhost:8080/convention/get -H "Content-Type: application/json" -d '{"host_id":"'"dummy_id"'"}'
echo -e "\n"

echo "Testing get convention by conv_id"
CONV_ID=$(jq -r '.conv_id' ./test_scripts/script_output.json)
echo $CONV_ID
curl -X POST http://localhost:8080/convention/get -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'"}'
echo -e "\n"

echo "Testing updating convention by conv_id"
curl -X PUT http://localhost:8080/convention/update -H "Content-Type: application/json" -d '{
    "id":"'"$CONV_ID"'",
    "start":"2025-11-16 13:00:00",
    "vendor_count":67
}'
echo -e "\n"
curl -X POST http://localhost:8080/convention/get -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'"}'
echo -e "\n"

echo "Testing delete convention by conv_id"
curl -X DELETE http://localhost:8080/convention/delete -H "Content-Type: application/json" -d '{"id":"'"$CONV_ID"'"}'
echo -e "\n"
curl -X POST http://localhost:8080/convention/get -H "Content-Type: application/json" -d '{}'
echo -e "\n"

docker compose down -v
