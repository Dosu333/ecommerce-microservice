import { createLogger, format, transports } from "winston";

const { combine, timestamp, printf, colorize, json } = format;

const logFormat = printf(({ level, message, timestamp, stack }) => {
  return `${timestamp} [${level.toUpperCase()}]: ${stack || message}`;
});

const logger = createLogger({
  level: "info",
  format: combine(
    timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
    json()
  ),
  transports: [
    new transports.Console({
      format: combine(colorize(), logFormat), // Colored logs in console
    }),
    new transports.File({ filename: "logs/error.log", level: "error" }), 
  ],
});

// If in development, log all levels
if (process.env.NODE_ENV !== "production") {
  logger.add(new transports.File({ filename: "logs/debug.log" }));
}

export default logger;
