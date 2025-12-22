FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
COPY .env .env

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]

