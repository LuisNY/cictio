#!/bin/sh

# Abort on any error (including if wait-for-it fails).
set -e

# Wait for the backend to be up, if we know where it is.
if [ -n "$MYSQL_HOST" ]; then
  /home/cictio-server/wait-for-it.sh "$MYSQL_HOST:${MYSQL_PORT:-6000}"
fi

# Run the main container command.
exec "$@"