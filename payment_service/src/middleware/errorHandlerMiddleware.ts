import { ValidationError, AuthenticationError, ForbiddenError } from "../errors/errors";
import { ValidationError as SequelizeValidationError, UniqueConstraintError } from "sequelize";

export const errorHandler = (err: Error, req: any, res: any, next: any) => {
    if (err instanceof ValidationError || err instanceof AuthenticationError || err instanceof ForbiddenError) {
        return res.status(err.statusCode).json({
            status: err.statusCode,
            message: err.message,
            details: err.details || null,
        })
    };

    if (err instanceof SequelizeValidationError) {
        return res.status(400).json({
            status: 400,
            message: "Validation error",
            details: err.errors.map((e) => e.message).join(", ")
        })
    };

    if (err instanceof UniqueConstraintError) {
        return res.status(400).json({
            status: 400,
            message: "Unique constraint violation",
            details: err.errors.map((e) => `${e.path}: ${e.value} already exists`).join(", ")
        });
    }

    return res.status(500).json({
        status: 500,
        message: err.message || "Internal Server Error",
        details: null,
    })
};