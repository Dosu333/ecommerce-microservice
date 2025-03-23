import express, { Application } from "express";
import { sequelize } from "./config/database";
import { connectRedis } from "./config/redis";
import cors from "cors";
import { errorHandler } from "./middleware/errorHandlerMiddleware";
import paymentRoutes from "./routes/paymentRoutes"
import walletRoutes from "./routes/walletRoutes"


const app: Application = express();
const allowedOrigins = [
  "http://localhost:5173", 
  "http://localhost:3000", 
]; // Add your allowed origins here

// Middleware
// app.use(express.json());
app.use(express.json({ limit: "10mb" })); // Adjust limit as needed
app.use(express.urlencoded({ limit: "10mb", extended: true }));
app.use(cors({
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));
app.use(errorHandler);


// Database Connection
(async () => {
  try {
    await sequelize.authenticate(); // Test connection
    console.log(
      "Connection to the database has been established successfully."
    );
    await sequelize.sync({ alter: true }); // Sync models, create/modify tables
    console.log("Database synced successfully.");
  } catch (error) {
    console.error("Unable to connect to the database:", error);
  }
})();

// Connect Redis
connectRedis();

// Routes
app.use("/payment", paymentRoutes)
app.use("/wallet", walletRoutes)

// Test connection
app.get("/", (req, res) => {
  res.status(200).send("This is the Payment Service");
});

// Error handling
app.use((err: any, req: any, res: any, next: any) => {
  console.error(err.stack);
  res.status(err.statusCode).send({
    status: err.statusCode,
    message: err.message || "Internal Server Error",
  });
});

export default app;
