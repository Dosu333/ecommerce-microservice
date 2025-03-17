#!/bin/sh

echo "Starting Payment Service Server with PM2..."
pm2 start npm --name "server" -- run start

echo "Waiting for server to initialize..."
sleep 5  # Adjust this time if necessary

echo "Starting Order Service Listener with PM2..."
pm2 start npm --name "orderListener" -- run orderListener

# Keep the container alive
pm2 logs
