#!/bin/bash

npm run build --fix 
rm -rf ../app/dist/
mv dist/ ../app/
