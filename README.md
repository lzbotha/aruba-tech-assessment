# Aplocation
aplocation = access point location, I know how to spell aplication ;)

## Env variables
The container needs the GEOLOCATION\_API\_KEY variable set with a valid Geolocation API key. Note that the docker-compose file will pass your local GEOLOCATION\_API\_KEY to the container.

## Testing
You can build the service using docker-compose. The service will be hosted on port 5000. I've included 2 scripts that I used to test the service with the example data.

### example_request.sh
hit the API with a very small lsit of access points.

### all_requests.sh
hit the API with all the access points provided in the example file.