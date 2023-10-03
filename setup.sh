#!/bin/bash
echo "You are using default database."
echo "If you want to change it put your .db file into sql-copilot/data directory"
echo "and change ENV variable PATH_TO_DATA in Dockerfile accordingly."

echo -e "\nBuilding docker container..."
docker build -t sql-copilot .
