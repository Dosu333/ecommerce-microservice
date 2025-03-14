# Use Node.js Alpine for a lightweight build
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the application files
COPY . .

# Expose the port for the service
EXPOSE 3000

# Run the service
CMD ["npm", "run", "start"]
