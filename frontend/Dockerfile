FROM node:20-alpine AS builder

WORKDIR /app
COPY frontend/package*.json ./
COPY silly-canny-lib ./silly-canny-lib/
RUN sed -i 's|"silly-canny-lib": "file:[^"]*"|"silly-canny-lib": "file:./silly-canny-lib"|g' package.json
RUN npm install --legacy-peer-deps
COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]