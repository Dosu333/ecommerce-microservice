import { Sequelize } from "sequelize";
import fs from "fs"
import path from "path";
import { DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER } from "./dotenv.config";

export const sequelize = new Sequelize(DB_NAME, DB_USER, DB_PASS, {
    host: DB_HOST,
    port: Number(DB_PORT),
    dialect: "postgres",
    logging: false
})