#!/bin/bash
sudo rm -rf venv
virtualenv venv
venv/bin/pip install -r requirements.txt
echo "MONGO_DETAILS=mongodb://localhost:27017" > .env