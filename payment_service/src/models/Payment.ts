import { Sequelize, DataTypes, Model } from "sequelize";

interface PaymentAttributes {
  id?: string;
  userId: string;
  orderId: string;
  reference?: string;
  amount: number;
  status?: string;
}

class Payment extends Model<PaymentAttributes> implements PaymentAttributes {
  public id!: string;
  public userId!: string;
  public orderId!: string;
  public reference?: string;
  public amount!: number;
  public status!: string;

  static initModel(sequelize: Sequelize): void {
    this.init(
      {
        id: {
          type: DataTypes.UUID,
          primaryKey: true,
          defaultValue: DataTypes.UUIDV4,
        },
        userId: {
          type: DataTypes.UUID,
          allowNull: false,
        },
        orderId: {
          type: DataTypes.UUID,
          allowNull: false,
        },
        reference: {
          type: DataTypes.STRING,
          unique: true,
        },
        amount: {
          type: DataTypes.INTEGER,
          allowNull: false,
        },
        status: {
          type: DataTypes.ENUM("pending", "success", "failed"),
          defaultValue: "pending",
        },
      },
      {
        sequelize,
        tableName: "payment",
        timestamps: true,
        hooks: {
          beforeCreate: (payment: Payment) => {
            payment.reference = `pay_${payment.id}`;
          },
        },
      }
    );
  }
}

export default Payment;
