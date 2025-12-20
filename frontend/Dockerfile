FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN cp .env.example .env && \
    sed -i 's|VITE_API_TARGET=.*|VITE_API_TARGET=http://backend:8000|' .env

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]

