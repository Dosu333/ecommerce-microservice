import { Sequelize, DataTypes, Model } from "sequelize";

interface WalletAttributes {
  id?: string;
  userId: string;
  balance?: number;
  currency?: string;
}

class Wallet extends Model<WalletAttributes> implements WalletAttributes {
  public id!: string;
  public userId!: string;
  public balance?: number;
  public currency?: string;

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
        balance: {
          type: DataTypes.DECIMAL,
          defaultValue: 0.00
        },
        currency: {
          type: DataTypes.STRING,
          defaultValue: "NGN"
        },
      },
      {
        sequelize,
        tableName: "wallet",
        timestamps: true,
      }
    );
  }
}

export default Wallet;
