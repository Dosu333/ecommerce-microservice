import { ValidationError } from "../errors/errors";
import { Op } from "sequelize";
import Escrow from "../models/Escrow";

export const getEscrowBalanceService = async (vendorId: string): Promise<number> => {
  if (!vendorId) {
    throw new ValidationError("Vendor ID is required");
  }

  const totalBalance = await Escrow.sum("amount", {
    where: {
      vendorId,
      status: { [Op.notIn]: ["released", "refunded"] },
    },
  });

  return totalBalance ?? 0.00;
};
