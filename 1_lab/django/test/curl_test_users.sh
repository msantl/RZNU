#!/bin/bash

# test GET on /users/
echo "test GET na /users/"
echo ""

echo "JSON svih korisnika"
curl -X GET localhost:8000/api/users/ -i
echo ""

# test POST on /users/
echo "test POST na /users/"
echo ""

echo "Bez administratorskih podataka"
curl -X POST localhost:8000/api/users/ -F"username=matija" -F"password=12345" -i
echo ""

echo "Bez polja s korisnickim imenom"
curl -X POST localhost:8000/api/users/ -u admin:12345 -F"password=12345" -i
echo ""

echo "Uspjesno stvaranje novog korisnika"
curl -X POST localhost:8000/api/users/ -u admin:12345 -F"username=matija" -F"password=12345" -i
echo ""

# test PUT on /users/
echo "test PUT na /users/"
echo ""

echo "Bez administratorskih podataka 1"
curl -X PUT localhost:8000/api/users/ -d id=2 -d username=mali -i
echo ""

echo "Bez administratorskih podataka 2"
curl -X PUT localhost:8000/api/users/ -u matija:12345 -d id=2 -i
echo ""

echo "Uspjesna promjena korisnickog imena"
curl -X PUT localhost:8000/api/users/ -u admin:12345 -d id=2 -d username=mali -i
echo ""

# test DELETE on /users/
echo "test DELETE na /users/"
echo ""

echo "Bez administratorskih podataka 1"
curl -X DELETE localhost:8000/api/users/ -i
echo ""

echo "Bez administratorskih podataka 2"
curl -X DELETE localhost:8000/api/users/ -u mali:12345 -i
echo ""

echo "Brisanje svih ne-administratorskih podataka"
curl -X DELETE localhost:8000/api/users/ -u admin:12345 -i
echo ""

