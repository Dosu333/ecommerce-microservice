import swaggerJSDoc from "swagger-jsdoc";

const swaggerDefinition = {
  openapi: "3.0.0",
  info: {
    title: "Payment Service Docs",
    version: "1.0.0",
    description: "API documentation for Payment service for ecommerce app",
  },
  servers: [
    {
      url: "http://localhost:3000",
      description: "Dev server",
    },
  ],
  components: {
    securitySchemes: {
      bearerAuth: {
        type: "http",
        scheme: "bearer",
        bearerFormat: "JWT",
      },
    },
  },
  security: [
    {
      bearerAuth: [],
    },
  ],
};

const options = {
  swaggerDefinition,
  apis: [__dirname + "/../../src/docs/*.ts", __dirname + "/../../src/docs/*.js"],
};

const swaggerSpec = swaggerJSDoc(options);

export default swaggerSpec;
