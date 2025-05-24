# ---------- Stage 1: build React (Vite) ----------
FROM node:20-alpine AS builder

# 1. Create working directory inside the container
WORKDIR /app

# 2. Copy only the dependency manifests first (enables Docker layer caching)
COPY package.json package-lock.json* ./
# 3. Install deps in CI mode (clean, reproducible)
RUN npm ci

# 4. Copy the rest of the source code
COPY . .

# 5. Build the static site into /app/dist
RUN npm run build


# ---------- Stage 2: serve with Nginx ----------
FROM nginx:1.27-alpine

# Copy the compiled assets from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
