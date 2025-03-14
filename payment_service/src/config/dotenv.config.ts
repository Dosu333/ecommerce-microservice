import dotenv from "dotenv";
import path from "path";

const envFilePath = path.resolve(__dirname, "../../.env");

// Load environment variables from the .env file
const result = dotenv.config({ path: envFilePath });

if (result.error) {
  throw new Error("Failed to load .env file");
}

export const NODE_ENV = process.env.NODE_ENV;
export const PORT = process.env.PORT || "3000";
export const DB_HOST = process.env.POSTGRES_HOST || "localhost";
export const DB_PORT = process.env.POSTGRES_PORT || "5432";
export const DB_USER = process.env.POSTGRES_USER || "ecommerceuser";
export const DB_PASS = process.env.POSTGRES_PASS || "ecommercepassword";
export const DB_NAME = process.env.POSTGRES_NAME || "ecommercedb";
export const JWT_SECRET = process.env.JWT_SECRET || "jwt_secret";
export const JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || "jwt_refresh_secret";
export const REDIS_HOST = process.env.REDIS_HOST || "localhost";
