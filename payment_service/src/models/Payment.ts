import { DataTypes, Model } from "sequelize";
import { sequelize } from "../config/database";


class Payment extends Model {}

Payment.init(
  {
    id: {
      type: DataTypes.UUID,
      primaryKey: true,
      defaultValue: DataTypes.UUIDV4,
    },
    user_id: { 
        type: DataTypes.UUID, 
        allowNull: false 
    },
    order_id: { 
        type: DataTypes.UUID, 
        allowNull: false 
    },
    reference: { 
        type: DataTypes.STRING, 
        unique: true, 
        allowNull: false 
    },
    amount: { 
        type: DataTypes.INTEGER, 
        allowNull: false 
    },
    status: {
      type: DataTypes.ENUM("pending", "success", "failed"),
      defaultValue: "pending",
    },
  },
  { 
    sequelize, 
    tableName: "payment",
    timestamps: true
 }
);

export default Payment;
