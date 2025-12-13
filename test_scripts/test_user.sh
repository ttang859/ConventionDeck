#!/usr/bin/env bash

docker compose up -d --build

# TEST 1
echo "Testing user create"
curl -X POST -H 'Content-Type: application/json' -d @./test_data/create_user.json http://localhost:8080/users/create
echo -e "\n"

# TEST 2
echo "Testing user get"
curl -o ./test_scripts/script_output.json -X GET http://localhost:8080/users/user/ttangvz859@gmail.com
curl -X GET http://localhost:8080/users/user/ttangvz859@gmail.com
echo -e "\n"

# TEST 3
echo "Testing user update"
USER_ID=$(jq -r '.id' ./test_scripts/script_output.json)
echo $USER_ID
curl -X PUT \
  -H 'Content-Type: application/json' \
  -d "{\"id\":\"$USER_ID\", \"username\":\"tyler\"}" \
  http://localhost:8080/users/update
echo -e "\n"
curl -X GET http://localhost:8080/users/user/ttangvz859@gmail.com
echo -e "\n"

docker compose down -v
