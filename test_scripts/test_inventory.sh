#!/usr/bin/env bash

docker compose up -d --build

# TEST 1
echo "Testing create new inventory entry"
# set up a user to attach item to
curl -X POST \
    -H 'Content-Type: application/json' \
    -d '{"email": "ttangvz859@gmail.com", "username":"tt", "user_type": "vendor"}' \
    http://localhost:8080/users/create
curl -o ./test_scripts/script_output.json -X GET http://localhost:8080/users/user/ttangvz859@gmail.com
USER_ID=$(jq -r '.id' ./test_scripts/script_output.json)
echo "Created user with ID: $USER_ID"
echo -e "\n"

# creates the item
curl -X POST \
-H 'Content-Type: application/json' \
-d "{\"owner_id\":\"$USER_ID\", \"card_name\":\"yuh\", \"price\":\"19.99\"}" \
http://localhost:8080/inventory/create
echo -e "\n"

# TEST 2
echo "Testing single item retrieval"
# this should return all of the items which is just one
curl -X POST \
-H 'Content-Type: application/json' \
http://localhost:8080/inventory/get
echo -e "\n"

# add another item
curl -X POST \
-H 'Content-Type: application/json' \
-d "{\"owner_id\":\"dummy_id\", \"card_name\":\"nah\", \"price\":\"79.99\"}" \
http://localhost:8080/inventory/create
echo -e "\n"

# this should return all of the items now
curl -X POST \
-H 'Content-Type: application/json' \
http://localhost:8080/inventory/get \
echo -e "\n"

# this should return the item associated with ttangvz859@gmail.com
curl -X POST \
-H 'Content-Type: application/json' \
-d "{\"owner_id\":\"$USER_ID\"}" \
http://localhost:8080/inventory/get
echo -e "\n"

# TEST 3
echo "Testing item update"
curl -X POST \
-o ./test_scripts/script_output.json \
-H 'Content-Type: application/json' \
-d "{\"owner_id\":\"$USER_ID\"}" \
http://localhost:8080/inventory/get
echo -e "\n"
ITEM_ID=$(jq -r '.payload[0].id' ./test_scripts/script_output.json)

# update price of item
curl -X PUT \
-H 'Content-Type: application/json' \
-d "{\"id\":\"$ITEM_ID\", \"price\":\"29.99\"}" \
http://localhost:8080/inventory/update
echo -e "\n"

# verify price of item has been updated
curl -X POST \
-H 'Content-Type: application/json' \
-d "{\"owner_id\":\"$USER_ID\"}" \
http://localhost:8080/inventory/get
echo -e "\n"

# TEST 4
echo "Testing item deletion"
curl -X DELETE \
-H 'Content-Type: application/json' \
-d "{\"id\":\"$ITEM_ID\"}" \
http://localhost:8080/inventory/delete
echo -e "\n"

# verify item has been deleted
curl -X POST \
-H 'Content-Type: application/json' \
-d "{\"owner_id\":\"$USER_ID\"}" \
http://localhost:8080/inventory/get
echo -e "\n"

docker compose down -v
