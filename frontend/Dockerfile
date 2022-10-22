FROM node:19-alpine3.15

WORKDIR /frontend

# Copy 'package.json' into working directory of container
COPY ./package.json .

# Install packages in package.json (React)
RUN npm install

# Copy in other files into working directory
# 'node_modules' excluded per '.dockerignore'
COPY . .

# Container runs on PORT 3000
EXPOSE 3000 

CMD ["npm", "start"]