import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { JWT_SECRET } from '../config/dotenv.config';

interface User {
    user_id: string;
    fullname: string;
    email: string;
    roles: string[];
}

export interface AuthenticatedRequest extends Request {
    user?: User;
};

export const authenticateUser = async (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        res.status(401).send({ status: 401, message: 'Missing or invalid token' });
        return;
    };

    const token = authHeader.split(" ")[1];

    try {
        const decoded: any = jwt.verify(token, JWT_SECRET);
        
        if (!decoded) {
            res.status(401).send({ status: 401, message: 'Invalid token' });
            return;
        }

        req.user = decoded;
        next();
    } catch (error) {
        res.status(401).send({ status: 401, message: 'Invalid token' });
        return;
    }
};