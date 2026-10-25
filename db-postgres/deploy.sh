#!/bin/bash

# Confirm with user before proceeding
read -p "This will stop and remove existing containers and volumes. Are you sure you want to continue? (y/n) " -n 1 -r
echo    # move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
   echo "Operation cancelled."
   exit 1
fi

docker compose down -v;
docker compose pull;
docker compose up -d --force-recreate --remove-orphans;

