#!/bin/bash

echo "Stvaram novog korisnika za potrebe test ..."
curl -X POST localhost:8000/api/users/ -u admin:12345 -F"username=matija" -F"password=12345" -i
echo ""

echo "Stvaram novi snippet za potrebe testa ..."
curl -X POST localhost:8000/api/snippets/ -u matija:12345 -F"title=naslov" -F"language=jezik" -F"source=izvorni kod" -i
echo ""

# test GET on /users/2
echo "test GET na /users/2"
echo ""

echo "Bez login podataka"
curl -X GET localhost:8000/api/users/2/ -i
echo ""

echo "JSON svih snippeta korisnika 2"
curl -X GET localhost:8000/api/users/2/ -u admin:12345 -i
echo ""

# test POST on /users/2
echo "test POST na /users/2"
echo ""

echo "Metoda nije dozvoljena"
curl -X POST localhost:8000/api/users/2/ -i
echo ""

# test PUT on /users/2
echo "test PUT na /users/2"
echo ""

echo "Bez login podataka"
curl -X PUT localhost:8000/api/users/2/ -d password=54321 -i
echo ""

echo "Bez odgovarajucih login podataka"
curl -X PUT localhost:8000/api/users/2/ -u admin:12345 -d password=54321 -i
echo ""

echo "Uspjesna promjena lozinke"
curl -X PUT localhost:8000/api/users/2/ -u matija:12345 -d password=54321 -i
echo ""

# test DELETE on /users/2
echo "test DELETE na /users/2"
echo ""

echo "Bez login podataka"
curl -X DELETE localhost:8000/api/users/2/ -i
echo ""

echo "Bez odgovorajucih login podataka"
curl -X DELETE localhost:8000/api/users/2/ -u admin:12345 -i
echo ""

echo "Uspjesno brisanje korisnika"
curl -X DELETE localhost:8000/api/users/2/ -u matija:54321 -i
echo ""

# maintenance
echo "Ciscenje ..."
curl -X DELETE localhost:8000/api/users/ -u admin:12345 -i
echo ""

