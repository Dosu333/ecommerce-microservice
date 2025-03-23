import { Sequelize } from "sequelize";
import { DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER } from "./dotenv.config";
import Payment from "../models/Payment";
import Wallet from "../models/Wallet";
import Escrow from "../models/Escrow";

export const sequelize = new Sequelize(DB_NAME, DB_USER, DB_PASS, {
    host: DB_HOST,
    port: Number(DB_PORT),
    dialect: "postgres",
    logging: false
})

Payment.initModel(sequelize)
Wallet.initModel(sequelize)
Escrow.initModel(sequelize)

export { Payment, Wallet, Escrow }