FROM node:14
WORKDIR /app
COPY ./standard-integration/package*.json ./
RUN npm install --production
COPY ./standard-integration .
CMD ["npm", "run", "production"]