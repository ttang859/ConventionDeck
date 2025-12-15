#!/usr/bin/env bash
docker compose up -d --build

echo "User setup"
curl -X POST http://localhost:8080/users/create -H "Content-Type: application/json" -d @./test_data/create_user.json
echo -e "\n"
curl -o ./test_scripts/script_output.json -X GET http://localhost:8080/users/user/ttangvz859@gmail.com
VID=$(jq -r '.id' ./test_scripts/script_output.json)

echo "Convention setup"
jq --arg key "host_id" --arg value "$VID" '. += {($key): $value}' ./test_data/create_convention.json > ./test_data/temp.json && mv ./test_data/temp.json ./test_data/create_convention.json
cat ./test_data/create_convention.json
curl -o test_scripts/script_output.json -X POST http://localhost:8080/convention/create -H "Content-Type: application/json" -d @./test_data/create_convention.json
echo -e "\n"
CONV_ID=$(jq -r '.conv_id' ./test_scripts/script_output.json)

echo "Booth Health Check"
curl -X GET http://localhost:8080/booth/health
echo -e "\n"

echo "Testing create booth"
curl -X POST http://localhost:8080/booth/create_all -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'","total_booths":"60"}'
echo -e "\n"

echo "Testing get booths by conv_id"
curl -X POST http://localhost:8080/booth/get -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'"}'
echo -e "\n"

echo "Testing assigning booth"
curl -X PUT http://localhost:8080/booth/assign_vendor -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "vendor_id":"'"$VID"'", "booth_number":"15"}'
echo -e "\n"

echo "Testing get booths by conv_id and vendor_id"
curl -X POST http://localhost:8080/booth/get -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "vendor_id":"'"$VID"'"}'
echo -e "\n"

echo "Adding dummy assignments"
curl -X PUT http://localhost:8080/booth/assign_vendor -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "vendor_id":"dummy_id", "booth_number":"30"}'
echo -e "\n"
curl -X PUT http://localhost:8080/booth/assign_vendor -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "vendor_id":"dummy_id2", "booth_number":"31"}'
echo -e "\n"
curl -X POST http://localhost:8080/booth/get -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'"}'
echo -e "\n"

echo "Testing unassignment of booth"
curl -X PUT http://localhost:8080/booth/unassign_vendor -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "booth_number":"15"}'
echo -e "\n"
curl -X POST http://localhost:8080/booth/get -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "vendor_id":"'"$VID"'"}'
echo -e "\n"

echo "Testing delete all booths by conv_id"
curl -X DELETE http://localhost:8080/booth/delete_all -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'", "total_booths":"60"}'
echo -e "\n"
curl -X POST http://localhost:8080/booth/get -H "Content-Type: application/json" -d '{"conv_id":"'"$CONV_ID"'"}'
echo -e "\n"

docker compose down -v
