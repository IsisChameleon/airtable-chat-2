#!/bin/bash

six_months_ago=$(date -d '6 months ago' +%s)

docker ps -a --format '{{.ID}}' | while read -r container_id; do
    last_started=$(docker inspect -f '{{.State.StartedAt}}' "$container_id" | xargs date +%s -d)
    if [ "$last_started" -lt "$six_months_ago" ]; then
        docker rm -f "$container_id"
    fi
done
