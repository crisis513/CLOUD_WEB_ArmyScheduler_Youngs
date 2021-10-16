#!/bin/bash

cd ../'WEB(FE)'
npm run build --fix 
rm -rf ../'WEB(BE)'/dist/
mv dist/ ../'WEB(BE)'/

cd ../'WEB(BE)'
venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 3000
