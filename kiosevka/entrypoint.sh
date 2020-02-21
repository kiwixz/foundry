#!/bin/sh

npm run build -- "$@"
chmod -R 777 "dist"
