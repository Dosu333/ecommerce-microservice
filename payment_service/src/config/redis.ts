import { createClient } from "redis";
import { REDIS_URL } from "./dotenv.config";


const redisClient = createClient({
  url: REDIS_URL || "redis://localhost:6379",
});

redisClient.on("error", (err) => console.error("Redis Error:", err));

redisClient.on("connect", () => console.log("Connected to Redis"));

export const connectRedis = async () => {
  if (!redisClient.isOpen) {
    await redisClient.connect();
  }
}

export default redisClient;
