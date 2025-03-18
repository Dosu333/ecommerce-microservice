import { Sequelize, DataTypes, Model } from "sequelize";

interface EscrowAttributes {
  id?: string;
  orderId: string; 
  buyerId: string;
  vendorId: string;
  amount?: number;
  status?: string;
}

class Escrow extends Model<EscrowAttributes> implements EscrowAttributes {
  public id!: string;
  public orderId!: string;
  public buyerId!: string;
  public vendorId!: string;
  public amount?: number;
  public status?: string;

  static initModel(sequelize: Sequelize): void {
    this.init(
      {
        id: {
          type: DataTypes.UUID,
          primaryKey: true,
          defaultValue: DataTypes.UUIDV4,
        },
        orderId: {
          type: DataTypes.UUID,
          allowNull: false,
        },
        buyerId: {
          type: DataTypes.UUID,
          allowNull: false,
        },
        vendorId: {
          type: DataTypes.UUID,
          allowNull: false,
        },
        amount: {
          type: DataTypes.DECIMAL,
          defaultValue: 0.00
        },
        status: {
          type: DataTypes.ENUM("pending", "released", "refunded"),
          defaultValue: "pending",
        },
      },
      {
        sequelize,
        tableName: "escrow",
        timestamps: true,
      }
    );
  }
}

export default Escrow;
