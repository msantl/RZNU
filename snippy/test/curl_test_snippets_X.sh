#!/bin/bash

echo "Stvaram novog korisnika za potrebe testa ..."
curl -X POST localhost:8000/api/users/ -u admin:12345 -F"username=matija" -F"password=12345" -i
echo ""

echo "Stvaram novi snippet za potrebe testa ..."
curl -X POST localhost:8000/api/snippets/ -u admin:12345 -F"title=naslov" -F"language=jezik" -F"source=izvorni kod" -i
echo ""

# test GET on /snippets/1/
echo "test GET na /snippets/1/"
echo ""

echo "Bez login podataka"
curl -X GET localhost:8000/api/snippets/1/ -i
echo ""

echo "JSON snippeta"
curl -X GET localhost:8000/api/snippets/1/ -u admin:12345 -i
echo ""

# test POST on /snippets/1/
echo "test POST na /snippets/1/"
echo ""

echo "Metoda nije dozvoljena"
curl -X POST localhost:8000/api/snippets/1/ -i 
echo ""

# test PUT on /snippets/1/
echo "test PUT na /snippets/1/"
echo ""

echo "Bez korisnickih podataka"
curl -X PUT localhost:8000/api/snippets/1/ -i
echo ""

echo "Bez odgovarajucih podataka"
curl -X PUT localhost:8000/api/snippets/1/ -u matija:12345 -i
echo ""

echo "Uspjesna promjena naslova"
curl -X PUT localhost:8000/api/snippets/1/ -u admin:12345 -d title=snippy -i
echo ""

# test DELETE on /snippets/1/
echo "test DELETE na /snippets/1/"
echo ""

echo "Bez korisnickih podataka"
curl -X DELETE localhost:8000/api/snippets/1/ -i
echo ""

echo "Bez odgovarajucih podataka"
curl -X DELETE localhost:8000/api/snippets/1/ -u matija:12345 -i
echo ""

echo "Uspjesno brisanje"
curl -X DELETE localhost:8000/api/snippets/1/ -u admin:12345 -i
echo ""

# maintenance
echo "Ciscenje ..."
curl -X DELETE localhost:8000/api/users/ -u admin:12345 -i
echo ""

