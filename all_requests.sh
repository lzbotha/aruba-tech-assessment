IFS=$'\n' # bash specific
for apscan in $(cat data/scan.json | jq -c '.[]'); do
    curl -i -H "Content-Type: application/json" -X POST --data "${apscan}" http://localhost:5000/api/v1.0/location
done