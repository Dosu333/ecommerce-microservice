import { Sequelize } from "sequelize";
import { DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER } from "./dotenv.config";
import Payment from "../models/Payment";

export const sequelize = new Sequelize(DB_NAME, DB_USER, DB_PASS, {
    host: DB_HOST,
    port: Number(DB_PORT),
    dialect: "postgres",
    logging: false
})

Payment.initModel(sequelize)

export { Payment }