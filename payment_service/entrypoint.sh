#!/bin/sh

echo "Starting Order Service Listener and Server with PM2..."
pm2 start npm --name "orderListener" -- run orderListener
pm2 start npm --name "server" -- run start

# Keep the container alive
pm2 logs
