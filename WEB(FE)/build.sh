#!/bin/bash

npm run build --fix 
rm -rf ../'WEB(BE)'/dist/
mv dist/ ../'WEB(BE)'/
