
This project will run on port 8025 in local dev by default

npm install flowbite
npx tailwindcss init tailwind.config.js
npx tailwindcss -i ./static/src/input_dj_polyglot_app.css -o ./static/src/output_dj_polyglot_app.css --watch


# Setup instructions for docker

### Step 1: Build Containers

Run the following command in your Yeoki directory: docker compose -f docker-compose.local.yml up --build

### Step 2: Connect to GitHub

Authenticate your GitHub account by running the following command in your terminal:: gh auth login

### Step 3: Clone the Repository

In VS Code, run: git clone https://github.com/Yeoki-ERP/dj_polyglot_app.git .

### Step 4: restart the containers