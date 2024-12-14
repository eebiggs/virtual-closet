FROM node:16-slim
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
RUN npm install -g sirv
EXPOSE 3000
CMD ["npx", "sirv", "public", "--host", "0.0.0.0"]


