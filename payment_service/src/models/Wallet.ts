import { Sequelize, DataTypes, Model } from "sequelize";

interface WalletAttributes {
  id?: string;
  userId: string;
  balance?: number;
  accountNumber?: string;
  bankName?: string;
  accountName?: string;
  bankCode?: string;
  recipientCode?: string;
  currency?: string;
}

class Wallet extends Model<WalletAttributes> implements WalletAttributes {
  public id!: string;
  public userId!: string;
  public balance?: number;
  public accountNumber?: string;
  public bankName?: string;
  public accountName?: string;
  public bankCode?: string;
  public recipientCode?: string;
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
          unique: true,
        },
        balance: {
          type: DataTypes.DECIMAL,
          defaultValue: 0.00
        },
        accountNumber: {
          type: DataTypes.STRING,
          allowNull: true,
        },
        bankName: {
          type: DataTypes.STRING,
          allowNull: true,
        },
        accountName: {
          type: DataTypes.STRING,
          allowNull: true,
        },
        bankCode: {
          type: DataTypes.STRING,
          allowNull: true,
        },
        recipientCode: {
          type: DataTypes.STRING,
          allowNull: true,
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
