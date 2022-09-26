#!/bin/bash
app="${APP_NAME:-skeleton}"
docker build --no-cache -t "${app}" .
docker run --rm -d -p 8080:80 --name="${app}" -v "$PWD"/app:/code/app "${app}"
