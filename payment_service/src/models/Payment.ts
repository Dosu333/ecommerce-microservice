import { Sequelize, DataTypes, Model } from "sequelize";

interface PaymentAttributes {
    id?: string;
    user_id: string;
    order_id: string;
    reference: string;
    amount: string;
    status?: string[];
}

class Payment extends Model<PaymentAttributes> implements PaymentAttributes {
    public id!: string;
    public user_id!: string;
    public order_id!: string;
    public reference!: string;
    public amount!: string;
    public status!: string[];
    
    static initModel(sequelize: Sequelize): void {
        this.init(
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
    }
}

export default Payment;
