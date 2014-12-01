#!/bin/bash

# test GET on /snippets/
echo "test GET na /snippets/"
echo ""

echo "JSON svih snippeta (bez sadrzaja)"
curl -X GET localhost:8000/api/snippets/ -i
echo ""

# test POST on /snippets/
echo "test POST na /snippets/"
echo ""

echo "Bez korisnickih podataka"
curl -X POST localhost:8000/api/snippets/ -i
echo ""

echo "Bez polja za izvorni kod"
curl -X POST localhost:8000/api/snippets/ -u admin:12345 -F"title=naslov" -F"language=jezik" -i
echo ""

echo "Uspjesno stvaranje novog snippeta"
curl -X POST localhost:8000/api/snippets/ -u admin:12345 -F"title=naslov" -F"language=jezik" -F"source=izvorni kod" -i
echo ""

# test PUT on /snippets/
echo "test PUT na /snippets/"
echo ""

echo "Bez korisnickih podataka"
curl -X PUT localhost:8000/api/snippets/ -i
echo ""

echo "Bez id oznake snippeta"
curl -X PUT localhost:8000/api/snippets/ -u admin:12345 -i
echo ""

echo "Uspjesna promjena naslova"
curl -X PUT localhost:8000/api/snippets/ -u admin:12345 -d snippet_id=1 -d title=snippy -i
echo ""

# test DELETE on /snippets/
echo "test DELETE na /snippets/"
echo ""

echo "Bez korisnickih podataka"
curl -X DELETE localhost:8000/api/snippets/ -i
echo ""

echo "Bez korisnickih oznaka administratora"
curl -X DELETE localhost:8000/api/snippets/ -u matija:12345 -i
echo ""

echo "Uspjesno brisanje svih snippeta iz sustava"
curl -X DELETE localhost:8000/api/snippets/ -u admin:12345 -i
echo ""


