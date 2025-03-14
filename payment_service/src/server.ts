import http from 'http';
import app from './app';
import { PORT } from './config/dotenv.config';


const server = http.createServer(app);

server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

process.on("unhandledRejection", (reason: any, promise: Promise<any>) => {
    console.error("Unhandled Rejection at:", promise, "reason:", reason);
});

process.on("uncaughtException", (error: any) => {
    console.error("Uncaught Exception:", error);
    process.exit(1);
})
