import { createClient } from "redis";
import { REDIS_URL } from "./dotenv.config";


const redisClient = createClient({
  url: REDIS_URL || "redis://localhost:6379",
});

redisClient.on("error", (err) => console.error("Redis Error:", err));

export default redisClient;
