class BaseError extends Error {
    public statusCode: number;
    public details?: any;

    constructor(message: string, statusCode: number, details?: any) {
        super(message);
        this.statusCode = statusCode;
        this.details = details;

        if (Error.captureStackTrace) {
            Error.captureStackTrace(this, this.constructor);
        }
    }
};

export class ValidationError extends BaseError {
    constructor(message: string, details?: any) {
        super(message, 400, details);
    }
};

export class AuthenticationError extends BaseError {
    constructor(message: string, details?: any) {
        super(message, 401, details);
    };
};

export class ForbiddenError extends BaseError {
    constructor(message: string, details?: any) {
        super(message, 403, details);
    }
}