#!/bin/bash

cd ../frontend
npm run build --fix 
rm -rf ../app/dist/
mv dist/ ../app/

cd ../app
venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 3000
