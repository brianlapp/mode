========================
CODE SNIPPETS
========================
TITLE: Example Output of Successful Distillery Release Build
DESCRIPTION: This snippet provides an example of the console output after a successful Distillery release build, showing confirmation of packaging and instructions for starting, connecting to, or getting help for the built release.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/phoenix-distillery.md#_snippet_14

LANGUAGE: Bash
CODE:
```
...
==> Packaging release..
Release successfully built!
To start the release you have built, you can use one of the following tasks:

    # start a shell, like 'iex -S mix'
    > _build/prod/rel/helloworld_distillery/bin/helloworld_distillery console

    # start in the foreground, like 'mix run --no-halt'
    > _build/prod/rel/helloworld_distillery/bin/helloworld_distillery foreground

    # start in the background, must be stopped with the 'stop' command
    > _build/prod/rel/helloworld_distillery/bin/helloworld_distillery start

If you started a release elsewhere, and wish to connect to it:

    # connects a local shell to the running node
    > _build/prod/rel/helloworld_distillery/bin/helloworld_distillery remote_console

    # connects directly to the running node's console
    > _build/prod/rel/helloworld_distillery/bin/helloworld_distillery attach

For a complete listing of commands and their use:

    > _build/prod/rel/helloworld_distillery/bin/helloworld_distillery help
```

----------------------------------------

TITLE: Specifying Start Command for Vite Applications
DESCRIPTION: This command serves a static site built with Vite, typically located in the `dist` directory, using the `serve` package. The `--single` flag is for single-page applications, and `--listen $PORT` ensures it listens on the correct port. The `serve` package must be installed as a dependency.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/errors/no-start-command-could-be-found.md#_snippet_7

LANGUAGE: bash
CODE:
```
serve --single --listen $PORT dist
```

----------------------------------------

TITLE: Specifying Start Command for Create React App Applications
DESCRIPTION: This command serves a static site built with Create React App, usually found in the `build` directory, using the `serve` package. The `--single` flag is for single-page applications, and `--listen $PORT` ensures it listens on the correct port. The `serve` package must be installed as a dependency.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/errors/no-start-command-could-be-found.md#_snippet_8

LANGUAGE: bash
CODE:
```
serve --single --listen $PORT build
```

----------------------------------------

TITLE: Installing Specific Apt Packages with Nixpacks (TOML)
DESCRIPTION: This TOML configuration snippet for Nixpacks specifies that the 'wget' package should be installed during the setup phase. This is achieved by listing 'wget' in the 'aptPkgs' array under the 'phases.setup' section of the Nixpacks configuration file.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/build-configuration.md#_snippet_3

LANGUAGE: toml
CODE:
```
[phases.setup]
    aptPkgs = ['wget']
```

----------------------------------------

TITLE: Adding Start Script to SvelteKit package.json
DESCRIPTION: This `package.json` snippet illustrates the addition of a `start` script, set to `node build/index.js`. This script is crucial for production environments, as it defines how the built SvelteKit application (located in the `build` directory) should be executed to start the server.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/sveltekit.md#_snippet_4

LANGUAGE: javascript
CODE:
```
{
	"name": "svelteapp",
	"version": "0.0.1",
	"type": "module",
	"scripts": {
		"dev": "vite dev",
		"build": "vite build",
		"start": "node build/index.js",
		"preview": "vite preview",
		"check": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json",
		"check:watch": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json --watch",
		"format": "prettier --write .",
		"lint": "prettier --check . && eslint ."
	},
	"devDependencies": {
		"@fontsource/fira-mono": "^5.0.0",
		"@neoconfetti/svelte": "^2.0.0",
		"@sveltejs/adapter-auto": "^3.0.0",
		"@sveltejs/adapter-node": "^5.2.9",
		"@sveltejs/kit": "^2.0.0",
		"@sveltejs/vite-plugin-svelte": "^4.0.0",
		"@types/eslint": "^9.6.0",
		"autoprefixer": "^10.4.20",
		"eslint": "^9.7.0",
		"eslint-config-prettier": "^9.1.0",
		"eslint-plugin-svelte": "^2.36.0",
		"globals": "^15.0.0",
		"prettier": "^3.3.2",
		"prettier-plugin-svelte": "^3.2.6",
		"prettier-plugin-tailwindcss": "^0.6.5",
		"svelte": "^5.0.0",
		"svelte-check": "^4.0.0",
		"tailwindcss": "^3.4.9",
		"typescript": "^5.0.0",
		"typescript-eslint": "^8.0.0",
		"vite": "^5.0.3"
	}
}
```

----------------------------------------

TITLE: Installing Railway CLI (npm)
DESCRIPTION: Installs the Railway Command Line Interface globally using npm, a package manager commonly used in JavaScript environments. This is the foundational step to interact with Railway services from your local machine.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/migration/migrate-from-vercel.md#_snippet_0

LANGUAGE: Shell
CODE:
```
npm i -g @railway/cli
```

----------------------------------------

TITLE: Set Start Command for Container Deployment
DESCRIPTION: Define the command to run when starting the container. This field can be set to `null`.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/config-as-code.md#_snippet_9

LANGUAGE: json
CODE:
```
{
  "$schema": "https://railway.com/railway.schema.json",
  "deploy": {
    "startCommand": "node index.js"
  }
}
```

----------------------------------------

TITLE: Configuring Rails App Start Command on Railway
DESCRIPTION: This command prepares the database by running migrations and then starts the Rails server, binding it to all available network interfaces. It's used as a custom start command in Railway to automate database setup and application launch.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/rails.md#_snippet_7

LANGUAGE: Shell
CODE:
```
bin/rails db:prepare && bin/rails server -b ::
```

----------------------------------------

TITLE: Example GitHub Actions Workflow for NuxtJS with Bun - YAML
DESCRIPTION: This YAML workflow defines a GitHub Action that runs an ESLint check on pull requests targeting the `main` branch. It utilizes self-hosted Railway runners, checks out the repository, installs Bun, sets up Node.js, caches dependencies, installs packages, and finally runs the lint command. It requires `contents: read` permission and uses specific GitHub Actions for checkout, Bun setup, Node setup, and caching.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/tutorials/github-actions-runners.md#_snippet_0

LANGUAGE: YAML
CODE:
```
name: eslint check

on:
  pull_request:
    branches:
      - main

permissions:
  contents: read

jobs:
  build:
    name: Check
    runs-on: [self-hosted, railway]

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Install bun
        uses: oven-sh/setup-bun@v2

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Cache Files
        uses: actions/cache@v4
        with:
          path: |
            ~/.bun/install/cache
            path: ${{ github.workspace }}/**/node_modules
            path: ${{ github.workspace }}/**/.nuxt
          key: ${{ runner.os }}-bun-${{ hashFiles('**/bun.lock', 'nuxt.config.ts', 'app.config.ts', 'app.vue') }}

      - name: Install packages
        run: bun install --prefer-offline

      - name: Lint
        run: bun run lint
```

----------------------------------------

TITLE: Initialize Node.js Project and Install Fastify Dependencies
DESCRIPTION: Initializes a new Node.js project with default settings and installs the Fastify and @fastify/etag packages using npm.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/tutorials/add-a-cdn-using-cloudfront.md#_snippet_0

LANGUAGE: plaintext
CODE:
```
npm init -y
npm i fastify @fastify/etag
```

----------------------------------------

TITLE: Configuring Nixpacks Start Command (TOML)
DESCRIPTION: This TOML configuration for Nixpacks specifies the command to start the application. It instructs Nixpacks to use Gunicorn to serve the Flask application, with `main:app` indicating the module and application instance to run.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/flask.md#_snippet_9

LANGUAGE: toml
CODE:
```
# nixpacks.toml

[start]
cmd = "gunicorn main:app"
```

----------------------------------------

TITLE: Serving Flask App with Gunicorn (Bash)
DESCRIPTION: This command starts the Gunicorn server to serve the Flask application. It assumes the Flask application instance is named `app` and is located in a file named `main.py` (or `helloworld.py` as per the example). It typically runs on `http://127.0.0.1:8000`.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/flask.md#_snippet_7

LANGUAGE: bash
CODE:
```
gunicorn main:app
```

----------------------------------------

TITLE: Add Custom NixPkgs to Nixpacks Plan Setup Phase
DESCRIPTION: Define specific options within the Nixpacks plan, such as adding custom Nix packages like `ffmpeg` to the setup phase.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/config-as-code.md#_snippet_6

LANGUAGE: json
CODE:
```
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "nixpacksPlan": {
      "phases": {
        "setup": {
          "nixPkgs": ["...", "ffmpeg"]
        }
      }
    }
  }
}
```

----------------------------------------

TITLE: Configuring Nixpacks Start Command (TOML)
DESCRIPTION: This `nixpacks.toml` configuration specifies the command Railway's Nixpacks build system uses to start the Clojure application. It first runs the standalone JAR with the `migrate` option to apply database migrations, then re-executes the JAR to launch the application. This ensures migrations are applied before the app starts serving requests.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/luminus.md#_snippet_4

LANGUAGE: toml
CODE:
```
# nixpacks.toml

[start]
cmd = "java -jar $(find ./target -name '*.jar' ! -name '*SNAPSHOT*') migrate && java -jar $(find ./target -name '*.jar' ! -name '*SNAPSHOT*')"
```

----------------------------------------

TITLE: Creating a New Remix App (Bash)
DESCRIPTION: This command initializes a new Remix application using `npx`. It requires Node.js to be installed and prompts the user for a directory name and whether to install dependencies automatically, setting up a new Remix project.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/remix.md#_snippet_0

LANGUAGE: Bash
CODE:
```
npx create-remix@latest
```

----------------------------------------

TITLE: Running SvelteKit App Locally
DESCRIPTION: This command starts the Vite development server for the SvelteKit application. It allows developers to preview and test their application locally, typically accessible via `http://localhost:5173` in a web browser.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/sveltekit.md#_snippet_1

LANGUAGE: bash
CODE:
```
npm run dev
```

----------------------------------------

TITLE: Installing React App Dependencies (Bash)
DESCRIPTION: After creating the React app, navigate into its directory and run this command to install all necessary project dependencies. This prepares the application for local development or deployment.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/react.md#_snippet_1

LANGUAGE: Bash
CODE:
```
npm install
```

----------------------------------------

TITLE: Creating a New Luminus App (Bash)
DESCRIPTION: This command initializes a new Luminus application named 'helloworld'. It includes support for PostgreSQL as the database and configures Immutant as the production-ready web server, optimizing it for Clojure applications. Ensure JDK and Leiningen are installed before running.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/luminus.md#_snippet_0

LANGUAGE: bash
CODE:
```
lein new luminus helloworld +postgres +immutant
```

----------------------------------------

TITLE: Configuring Nixpacks for Elixir Phoenix Deployment
DESCRIPTION: This `nixpacks.toml` file defines the build and deployment process for an Elixir Phoenix application. It specifies environment variables, required Nix packages, installation commands for dependencies, build commands for compilation and asset deployment, and the final command to start the server and set up the database.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/phoenix.md#_snippet_4

LANGUAGE: TOML
CODE:
```
[variables]
MIX_ENV = 'prod'

[phases.setup]
nixPkgs = ['...', 'erlang']

[phases.install]
cmds = [
  'mix local.hex --force',
  'mix local.rebar --force',
  'mix deps.get --only prod'
]

[phases.build]
cmds = [
  'mix compile',
  'mix assets.deploy'
]

[start]
cmd = "mix ecto.setup && mix phx.server"
```

----------------------------------------

TITLE: Cloning the Example Terraform Project in Bash
DESCRIPTION: This command clones the example Terraform project from GitHub, which contains the necessary configurations to stand up AWS resources for testing connectivity to RDS. This project serves as a starting point for deploying the Tailscale bridge.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/tutorials/bridge-railway-to-rds-with-tailscale.md#_snippet_1

LANGUAGE: bash
CODE:
```
git clone git@github.com:echohack/rds-tailscale.git
```

----------------------------------------

TITLE: Containerizing a Fastify App with Dockerfile for Railway
DESCRIPTION: This Dockerfile defines the steps to build a Docker image for a Fastify Node.js application, enabling its deployment on Railway. It uses the `node:18-alpine` base image, sets the working directory, copies application files, installs Node.js dependencies using `npm ci`, and specifies `npm start` as the command to run the web service upon container startup. This setup ensures the application is self-contained and portable for Railway's Docker-based deployment.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/fastify.md#_snippet_0

LANGUAGE: Dockerfile
CODE:
```
# Use the Node.js 18 alpine official image
# https://hub.docker.com/_/node
FROM node:18-alpine

# Create and change to the app directory.
WORKDIR /app

# Copy local code to the container image.
COPY . .

# Install project dependencies
RUN npm ci

# Run the web service on container startup.
CMD ["npm", "start"]
```

----------------------------------------

TITLE: Installing SolidJS App Dependencies (npm)
DESCRIPTION: After navigating into the newly created SolidJS project directory, this command installs all necessary project dependencies defined in the `package.json` file. This is a standard step before running or building any Node.js-based application.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/solid.md#_snippet_1

LANGUAGE: Bash
CODE:
```
npm install
```

----------------------------------------

TITLE: Wrapping Start Command with Shell for Environment Variables - Shell
DESCRIPTION: This shell command demonstrates how to wrap a Python application's start command to enable environment variable expansion, specifically for services deployed from a Dockerfile or image. This is necessary because commands executed in 'exec' form do not inherently support variable expansion, requiring a shell wrapper to interpret variables like `$PORT`.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/build-and-start-commands.md#_snippet_0

LANGUAGE: shell
CODE:
```
/bin/sh -c "exec python main.py --port $PORT"
```

----------------------------------------

TITLE: Initializing Railway Project (Bash)
DESCRIPTION: This command initializes a new Railway project within the current Nuxt application directory. It guides the user through prompts to name the project and provides a link to view it in the browser after creation. Requires Railway CLI to be installed and authenticated.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/nuxt.md#_snippet_2

LANGUAGE: bash
CODE:
```
railway init
```

----------------------------------------

TITLE: Specifying Start Command for FastAPI Applications
DESCRIPTION: This command starts a FastAPI application using Uvicorn, binding it to all available network interfaces (`0.0.0.0`) and the port specified by the `$PORT` environment variable. `main:app` refers to the `app` variable within the `main.py` file, which should be adjusted to match your application's structure.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/errors/no-start-command-could-be-found.md#_snippet_3

LANGUAGE: bash
CODE:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

----------------------------------------

TITLE: Running Node.js Project with Railway Environment Variables (Bash)
DESCRIPTION: An example demonstrating how to run a Node.js project locally using `npm start`, with all remote environment variables from the linked Railway project automatically applied.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/cli.md#_snippet_12

LANGUAGE: bash
CODE:
```
railway run npm start
```

----------------------------------------

TITLE: Creating a New Phoenix Application - Bash
DESCRIPTION: This command generates a new Phoenix application named 'helloworld' in the current directory. It sets up the basic project structure and prompts the user to install optional dependencies like Ecto and Phoenix LiveView.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/phoenix.md#_snippet_1

LANGUAGE: bash
CODE:
```
mix phx.new helloworld
```

----------------------------------------

TITLE: Starting React Development Server (Bash)
DESCRIPTION: This command starts the Vite development server, making your React application accessible locally, typically at 'http://localhost:5173'. It's used for local testing and development.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/react.md#_snippet_2

LANGUAGE: Bash
CODE:
```
npm run dev
```

----------------------------------------

TITLE: Installing Flask (Bash)
DESCRIPTION: This command installs the Flask web framework into the active virtual environment using pip. Flask is a microframework for building web applications in Python.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/flask.md#_snippet_3

LANGUAGE: bash
CODE:
```
python -m pip install flask
```

----------------------------------------

TITLE: Running Play Application Locally
DESCRIPTION: This SBT command builds the Play project, installs dependencies, and starts the embedded Pekko HTTP server. It allows developers to run and test the Play application locally, accessible via `http://localhost:9000`.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/play.md#_snippet_10

LANGUAGE: Bash
CODE:
```
sbt run
```

----------------------------------------

TITLE: Running Application with Production Variables (Railway CLI)
DESCRIPTION: Starts your application locally while automatically injecting environment variables from your Railway production environment. This crucial step helps maintain development/production parity and allows for early detection of environment-specific issues.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/migration/migrate-from-vercel.md#_snippet_2

LANGUAGE: Shell
CODE:
```
railway run
```

----------------------------------------

TITLE: Creating a Dockerfile for Node.js Remix App Deployment
DESCRIPTION: This Dockerfile defines the build process for a Node.js Remix application, starting from a Node.js Alpine base image. It sets up the working directory, copies dependencies, installs packages, copies application code, builds the application, and specifies the command to start the server. Railway automatically detects and uses this Dockerfile for building and deploying the app.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/remix.md#_snippet_4

LANGUAGE: Dockerfile
CODE:
```
# Use the Node alpine official image
# https://hub.docker.com/_/node
FROM node:lts-alpine

# Create and change to the app directory.
WORKDIR /app

# Copy the files to the container image
COPY package*.json ./

# Install packages
RUN npm ci

# Copy local code to the container image.
COPY . ./

# Build the app.
RUN npm run build
    
# Serve the app
CMD ["npm", "run", "start"]
```

----------------------------------------

TITLE: Specifying Start Command for Django Applications
DESCRIPTION: This command starts a Django application using Gunicorn, serving the WSGI application. `myproject.wsgi` refers to the `wsgi.py` file located within your Django project's main folder, which should be replaced with your actual project name.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/errors/no-start-command-could-be-found.md#_snippet_5

LANGUAGE: bash
CODE:
```
gunicorn myproject.wsgi
```

----------------------------------------

TITLE: Starting Symfony App Service with Nginx and Migrations (Bash)
DESCRIPTION: This Bash script is executed to start the Symfony application service. It first runs database migrations using `doctrine:migrations:migrate`, then processes an Nginx configuration template, and finally starts both PHP-FPM and Nginx to serve the application. It ensures the app is ready after the build phase.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/symfony.md#_snippet_12

LANGUAGE: Bash
CODE:
```
#!/bin/bash
# Make sure this file has executable permissions, run `chmod +x run-app.sh`
# Run migrations, process the Nginx configuration template and start Nginx
php bin/console doctrine:migrations:migrate --no-interaction && node /assets/scripts/prestart.mjs /assets/nginx.template.conf /nginx.conf && (php-fpm -y /assets/php-fpm.conf & nginx -c /nginx.conf)
```

----------------------------------------

TITLE: Starting an Express Application Locally (Bash)
DESCRIPTION: This command initiates the Express application locally. It executes the `start` script defined in the `package.json` file, typically launching the Node.js server. The application will then be accessible via a web browser, usually at `http://localhost:3000`.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/express.md#_snippet_1

LANGUAGE: Bash
CODE:
```
npm start
```

----------------------------------------

TITLE: Setting Start Command for MongoDB Exporter on Railway
DESCRIPTION: This snippet provides the start command for the `mongo-exporter` service. It executes the `mongodb_exporter` binary, enabling debug logging and instructing it to collect all available MongoDB metrics, which are then exposed on a `/metrics` endpoint.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/tutorials/deploy-and-monitor-mongo.md#_snippet_7

LANGUAGE: plaintext
CODE:
```
/mongodb_exporter --log.level="debug" --collect-all
```

----------------------------------------

TITLE: Configure Pre-deploy Command in Railway JSON
DESCRIPTION: Specify a command to execute before the container starts during deployment. This ensures necessary setup, like database migrations, is completed. This field is optional and can be omitted if no pre-deployment steps are required.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/config-as-code.md#_snippet_10

LANGUAGE: json
CODE:
```
{
  "$schema": "https://railway.com/railway.schema.json",
  "deploy": {
    "preDeployCommand": ["npm run db:migrate"]
  }
}
```

----------------------------------------

TITLE: Configure Custom Install Command in Nixpacks Plan
DESCRIPTION: Use the Nixpacks plan to configure a custom install command for your project.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/config-as-code.md#_snippet_7

LANGUAGE: json
CODE:
```
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "nixpacksPlan": {
      "phases": {
        "install": {
          "dependsOn": ["setup"],
          "cmds": ["npm install --legacy-peer-deps"]
        }
      }
    }
  }
}
```

----------------------------------------

TITLE: Starting a NestJS Application Locally (NPM)
DESCRIPTION: This command starts the NestJS application locally, typically making it accessible at 'http://localhost:3000'. It utilizes the 'start' script defined in the project's 'package.json' file.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/nest.md#_snippet_1

LANGUAGE: Bash
CODE:
```
npm run start
```

----------------------------------------

TITLE: Initializing Railway Project with CLI (Bash)
DESCRIPTION: This command is used to initialize a new Railway project from your SvelteKit app directory. It guides you through naming your project and provides a link to view it in your browser upon creation. This is a prerequisite for deploying via the CLI.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/sveltekit.md#_snippet_5

LANGUAGE: bash
CODE:
```
railway init
```

----------------------------------------

TITLE: Starting the Symfony Local Development Server (Bash)
DESCRIPTION: This command initiates the built-in Symfony web server, making the application accessible locally. It's used for testing and development purposes before deployment.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/symfony.md#_snippet_1

LANGUAGE: bash
CODE:
```
symfony server:start
```

----------------------------------------

TITLE: Configuring Nixpacks for Phoenix Distillery Deployment - TOML
DESCRIPTION: This `nixpacks.toml` configuration file defines the build and start phases for a Phoenix Distillery application on Railway. It sets `MIX_ENV` to `prod`, specifies Erlang as a dependency, and includes commands for dependency installation, compilation, asset digestion, release creation, and application startup.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/phoenix-distillery.md#_snippet_18

LANGUAGE: toml
CODE:
```
# nixpacks.toml
[variables]
MIX_ENV = 'prod'

[phases.setup]
nixPkgs = ['...', 'erlang']

[phases.install]
cmds = [
  'mix local.hex --force',
  'mix local.rebar --force',
  'mix deps.get --only prod'
]

[phases.build]
cmds = [
  'mix compile',
  'mkdir -p _build/prod/rel/helloworld_distillery/releases/RELEASES',
  'mix do phx.digest, distillery.release --env=prod',
]

[start]
cmd = "mix ecto.setup && _build/prod/rel/helloworld_distillery/bin/helloworld_distillery foreground"
```

----------------------------------------

TITLE: Installing Django Framework - Bash
DESCRIPTION: This command uses pip, Python's package installer, to install the Django web framework into the active virtual environment. Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/django.md#_snippet_2

LANGUAGE: Bash
CODE:
```
python -m pip install django
```

----------------------------------------

TITLE: Running a Rust Rocket Application Locally (Bash)
DESCRIPTION: This command compiles and runs the Rust Rocket application locally using Cargo. It installs any necessary dependencies and starts the web server, making the application accessible typically at `http://localhost:8000`.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/rocket.md#_snippet_3

LANGUAGE: bash
CODE:
```
cargo run
```

----------------------------------------

TITLE: Defining a Basic Rocket Web Server (Rust)
DESCRIPTION: This Rust code defines a minimal web server using the Rocket framework. It sets up a GET route for the root URL (`/`) that returns 'Hello world, Rocket!' and initializes the Rocket application to serve this route. It demonstrates basic routing and response handling.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/rocket.md#_snippet_2

LANGUAGE: rust
CODE:
```
#[macro_use] 
extern crate rocket;

#[get("/")]
fn index() -> &'static str {
    "Hello world, Rocket!"
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![index])
}
```

----------------------------------------

TITLE: Initializing a Railway Project with CLI
DESCRIPTION: This command initializes a new Railway project within your current application directory. It guides you through naming the project and provides a link to view it in the browser upon creation.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/play.md#_snippet_16

LANGUAGE: bash
CODE:
```
railway init
```

----------------------------------------

TITLE: Installing Production Dependencies - Bash
DESCRIPTION: This command installs `gunicorn` (a production-ready WSGI server), `whitenoise` (for serving static files efficiently), and `psycopg[binary,pool]` (a robust PostgreSQL adapter for Python) into the project's virtual environment, preparing the application for deployment.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/django.md#_snippet_4

LANGUAGE: Bash
CODE:
```
python -m pip install gunicorn whitenoise psycopg[binary,pool]
```

----------------------------------------

TITLE: Installing Railway CLI via npm (Cross-Platform)
DESCRIPTION: Installs the Railway CLI globally using npm, making it available across macOS, Linux, and Windows. This method requires Node.js version 16 or higher to be installed on your system.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/cli.md#_snippet_1

LANGUAGE: bash
CODE:
```
npm i -g @railway/cli
```

----------------------------------------

TITLE: Modifying Astro Start Script in package.json (JSON)
DESCRIPTION: This `package.json` snippet shows the updated `start` script for an Astro application configured for SSR. The `start` script is changed from `astro dev` to `node ./dist/server/entry.mjs`, directing Node.js to execute the server entry point generated after the build process, which is essential for running the server in `standalone` mode.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/astro.md#_snippet_4

LANGUAGE: json
CODE:
```
{
    "name": "astroblog",
    "type": "module",
    "version": "0.0.1",
    "scripts": {
        "dev": "astro dev",
        "start": "node ./dist/server/entry.mjs",
        "build": "astro check && astro build",
        "preview": "astro preview",
        "astro": "astro"
    },
    "dependencies": {
        "@astrojs/check": "^0.9.4",
        "@astrojs/mdx": "^3.1.8",
        "@astrojs/node": "^8.3.4",
        "@astrojs/rss": "^4.0.9",
        "@astrojs/sitemap": "^3.2.1",
        "astro": "^4.16.6",
        "typescript": "^5.6.3"
    }
}
```

----------------------------------------

TITLE: Specifying Start Command for Next.js Applications
DESCRIPTION: This command starts a Next.js production server, ensuring it listens on the port specified by the `$PORT` environment variable. The `--port` flag is crucial for Next.js to bind to the correct port in the Railway environment.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/errors/no-start-command-could-be-found.md#_snippet_1

LANGUAGE: bash
CODE:
```
npx next start --port $PORT
```

----------------------------------------

TITLE: Starting Phoenix Development Server - Bash
DESCRIPTION: This command starts the Phoenix application's development server. By default, the server listens for requests on port `4000`, allowing local testing and interaction with the application via a web browser.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/phoenix.md#_snippet_3

LANGUAGE: bash
CODE:
```
mix phx.server
```

----------------------------------------

TITLE: Creating a New Beego Application with Bee Tool
DESCRIPTION: This command sequence initializes a new Beego project named 'helloworld', navigates into its directory, and then tidies up Go module dependencies. It's the standard way to set up a new Beego application.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/beego.md#_snippet_0

LANGUAGE: bash
CODE:
```
bee new helloworld
cd helloworld
go mod tidy
```

----------------------------------------

TITLE: Starting Phoenix Distillery Release Locally - Bash
DESCRIPTION: This command starts the compiled Phoenix application in the foreground, allowing for local testing. It executes the release binary generated by Distillery in production mode.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/phoenix-distillery.md#_snippet_17

LANGUAGE: bash
CODE:
```
_build/prod/rel/helloworld_distillery/bin/helloworld_distillery foreground
```

----------------------------------------

TITLE: Creating a Dockerfile for NestJS Deployment on Railway
DESCRIPTION: This Dockerfile defines the build and runtime environment for a NestJS application. It uses a Node LTS image, sets up the working directory, copies application code, installs dependencies using 'npm ci', and specifies the production start command for the application.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/nest.md#_snippet_13

LANGUAGE: Dockerfile
CODE:
```
# Use the Node official image
# https://hub.docker.com/_/node
FROM node:lts

# Create and change to the app directory.
WORKDIR /app

# Copy local code to the container image
COPY . ./

# Install packages
RUN npm ci

# Serve the app
CMD ["npm", "run", "start:prod"]
```

----------------------------------------

TITLE: Adding Node SSR Adapter to Astro (Bash)
DESCRIPTION: This command installs the Node.js adapter for Astro, enabling Server-Side Rendering (SSR) capabilities for the application. It also automatically updates the `astro.config.mjs` file to reflect the new adapter configuration, streamlining the SSR setup process.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/astro.md#_snippet_2

LANGUAGE: bash
CODE:
```
npx astro add node
```

----------------------------------------

TITLE: Creating a New Railway Project via CLI
DESCRIPTION: This `plaintext` command initializes a new project using the Railway CLI. Users will be prompted to name their project, facilitating the setup of a new deployment environment on Railway.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/tutorials/set-up-a-datadog-agent.md#_snippet_6

LANGUAGE: plaintext
CODE:
```
railway init
```

----------------------------------------

TITLE: Creating a New React App with Vite (Bash)
DESCRIPTION: This command uses Vite to scaffold a new React project. It creates a new directory named 'helloworld' and populates it with a basic React application structure. This step requires Node.js to be installed on your machine.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/react.md#_snippet_0

LANGUAGE: Bash
CODE:
```
npm create vite@latest helloworld -- --template react
```

----------------------------------------

TITLE: Specifying Start Command for Node.js Applications
DESCRIPTION: This command runs a Node.js application by executing its main entry point file. The `main.js` file should be replaced with the actual entry point of your application, such as `index.js`, `server.js`, or `app.js`.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/errors/no-start-command-could-be-found.md#_snippet_0

LANGUAGE: bash
CODE:
```
node main.js
```

----------------------------------------

TITLE: Starting the Rails Development Server
DESCRIPTION: This command starts the Rails development server, typically WEBrick or Puma, allowing the application to be accessed locally. It binds the server to `http://localhost:3000` by default, enabling local testing and development of the Rails application.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/rails.md#_snippet_4

LANGUAGE: bash
CODE:
```
bin/rails server
```

----------------------------------------

TITLE: Specifying Start Command for Ruby on Rails Applications
DESCRIPTION: This command starts a Ruby on Rails server, binding it to all network interfaces (`0.0.0.0`) and the port specified by the `$PORT` environment variable. The `-b` and `-p` flags are essential for ensuring the Rails server listens on the correct host and port in the deployment environment.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/errors/no-start-command-could-be-found.md#_snippet_6

LANGUAGE: bash
CODE:
```
bundle exec rails server -b 0.0.0.0 -p $PORT
```

----------------------------------------

TITLE: Specifying Start Command for Nuxt.js Applications
DESCRIPTION: This command runs a Nuxt.js application in production mode, leveraging its built-in Nitro server. It directly executes the compiled server entry point located in the `.output/server/` directory.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/errors/no-start-command-could-be-found.md#_snippet_2

LANGUAGE: bash
CODE:
```
node .output/server/index.mjs
```

----------------------------------------

TITLE: Installing Vue App Dependencies (Bash)
DESCRIPTION: After navigating into the newly created Vue project directory, this command installs all necessary project dependencies defined in the `package.json` file. This prepares the application for local development or deployment.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/vue.md#_snippet_1

LANGUAGE: bash
CODE:
```
npm install
```

----------------------------------------

TITLE: Starting NestJS Application on a Custom Port (NPM)
DESCRIPTION: This command starts the NestJS application locally on a specified port, such as 8080. It achieves this by setting the 'PORT' environment variable before executing the 'npm run start' command.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/nest.md#_snippet_2

LANGUAGE: Bash
CODE:
```
PORT=8080 npm run start
```

----------------------------------------

TITLE: Specifying Start Command for Flask Applications
DESCRIPTION: This command starts a Flask application using Gunicorn, a WSGI HTTP server. `main:app` indicates that the Flask application object named `app` is located within the `main.py` file, which should be updated to reflect your actual file and variable names.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/errors/no-start-command-could-be-found.md#_snippet_4

LANGUAGE: bash
CODE:
```
gunicorn main:app
```

----------------------------------------

TITLE: Installing Sails CLI Globally (Bash)
DESCRIPTION: This command installs the Sails.js command-line interface globally on your system using npm. Installing it globally allows you to use the `sails` command from any directory to create and manage Sails applications. It is a prerequisite for generating new Sails projects.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/sails.md#_snippet_0

LANGUAGE: Bash
CODE:
```
npm install sails -g
```

----------------------------------------

TITLE: Initializing a New Railway Project with CLI
DESCRIPTION: This command initializes a new, empty project on Railway directly from the command line. It sets up the project context for any subsequent CLI commands, linking your local code to a remote Railway project.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/quick-start.md#_snippet_0

LANGUAGE: Shell
CODE:
```
railway init
```

----------------------------------------

TITLE: Installing SvelteKit Node Adapter
DESCRIPTION: This command installs the `@sveltejs/adapter-node` package as a development dependency. The Node adapter is essential for building and deploying SvelteKit applications to Node.js environments, converting the built app into a format suitable for server-side execution.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/sveltekit.md#_snippet_2

LANGUAGE: bash
CODE:
```
npm i -D @sveltejs/adapter-node
```

----------------------------------------

TITLE: Configuring Laravel Worker Service Start Command (Bash)
DESCRIPTION: This command is used as a custom start command for the worker service on Railway. It first grants execute permissions to the `run-worker.sh` script and then executes it, ensuring the worker process starts correctly. This is crucial for processing queued jobs.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/laravel.md#_snippet_3

LANGUAGE: bash
CODE:
```
chmod +x ./run-worker.sh && sh ./run-worker.sh
```

----------------------------------------

TITLE: Installing Phoenix Application Generator - Bash
DESCRIPTION: This command installs the Phoenix application generator using the Hex package manager. It is a prerequisite for creating new Phoenix projects.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/phoenix-distillery.md#_snippet_0

LANGUAGE: bash
CODE:
```
mix archive.install hex phx_new
```

----------------------------------------

TITLE: Installing Phoenix Application Generator - Bash
DESCRIPTION: This command installs the Phoenix application generator globally using the Hex package manager. It is a necessary prerequisite for creating new Phoenix projects on your machine.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/phoenix.md#_snippet_0

LANGUAGE: bash
CODE:
```
mix archive.install hex phx_new
```

----------------------------------------

TITLE: Running Rust Axum App Locally
DESCRIPTION: Executing this command in the project directory compiles the Rust Axum application, resolves and installs any missing dependencies, and then launches the web server. Once running, the application will be accessible locally, typically at `http://localhost:3000`.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/axum.md#_snippet_3

LANGUAGE: bash
CODE:
```
cargo run
```

----------------------------------------

TITLE: Creating a New Rust Axum Project
DESCRIPTION: This command initializes a new binary-based Cargo project named `helloworld`. It sets up the basic directory structure and `Cargo.toml` file, preparing the environment for a new Rust Axum application.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/axum.md#_snippet_0

LANGUAGE: bash
CODE:
```
cargo new helloworld --bin
```

----------------------------------------

TITLE: Installing Gunicorn Production Server (Bash)
DESCRIPTION: This command installs Gunicorn, a production-ready WSGI HTTP server for Python web applications. Gunicorn is recommended for serving Flask applications in a production environment due to its robustness and performance.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/flask.md#_snippet_6

LANGUAGE: bash
CODE:
```
pip install gunicorn
```

----------------------------------------

TITLE: Starting Vue App Development Server (Bash)
DESCRIPTION: This command starts the Vite development server for the Vue application, typically making it accessible on `http://localhost:5173`. It enables live reloading and hot module replacement for efficient local development.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/vue.md#_snippet_2

LANGUAGE: bash
CODE:
```
npm run dev
```

----------------------------------------

TITLE: Starting Mongo Docker with IPv6/IPv4 Bindings (Bash)
DESCRIPTION: This command demonstrates how to start the official Mongo Docker container to listen on both IPv6 and IPv4 addresses. It uses the `--ipv6` flag and sets `bind_ip` to `::,0.0.0.0` to enable dual-stack listening, essential for private network connectivity.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/private-networking.md#_snippet_11

LANGUAGE: bash
CODE:
```
docker-entrypoint.sh mongod --ipv6 --bind_ip ::,0.0.0.0
```

----------------------------------------

TITLE: Running Remix App Locally (Bash)
DESCRIPTION: This command starts the Vite development server for a Remix application. It allows developers to preview their app locally, typically accessible via `http://localhost:5173` in a web browser.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/remix.md#_snippet_1

LANGUAGE: Bash
CODE:
```
npm run dev
```

----------------------------------------

TITLE: Initializing a Railway Project with CLI (Bash)
DESCRIPTION: This command initializes a new Railway project in the current directory. It prompts the user to name the project and provides a link to view it in the browser after creation. This is the first step in setting up a new application on Railway using the CLI.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/beego.md#_snippet_5

LANGUAGE: bash
CODE:
```
railway init
```

----------------------------------------

TITLE: Running Flask App Locally (Bash)
DESCRIPTION: This command starts the Flask development server, running the `helloworld.py` application. It allows local testing and debugging of the Flask application, typically accessible at `http://127.0.0.1:5000`.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/flask.md#_snippet_5

LANGUAGE: bash
CODE:
```
flask --app helloworld run
```

----------------------------------------

TITLE: Initializing Railway Project (CLI)
DESCRIPTION: This command initializes a new Railway project within the current SolidJS application directory. It guides the user through prompts to name the project and sets up the necessary configuration for deploying the application to Railway via the CLI.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/solid.md#_snippet_3

LANGUAGE: Bash
CODE:
```
railway init
```

----------------------------------------

TITLE: Installing Railway CLI via Scoop (Windows)
DESCRIPTION: Installs the Railway CLI as a native Windows executable using the Scoop package manager. This provides a convenient way to manage the CLI on Windows systems.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/cli.md#_snippet_3

LANGUAGE: powershell
CODE:
```
scoop install railway
```

----------------------------------------

TITLE: Configuring Worker Service Custom Start Command (Shell)
DESCRIPTION: This shell command is configured as the custom start command for the Worker Service on Railway. It first grants execute permissions to the `run-worker.sh` script and then executes it. This ensures the worker process, responsible for handling queued jobs, starts correctly upon deployment.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/symfony.md#_snippet_15

LANGUAGE: Shell
CODE:
```
chmod +x ./run-worker.sh && sh ./run-worker.sh
```

----------------------------------------

TITLE: Building and Running a Gin App with Dockerfile
DESCRIPTION: This Dockerfile defines the steps to build and run a Gin (Go) application within a Docker container. It uses the official Go Alpine image, sets up the working directory, copies Go module files and source code, downloads dependencies, builds the executable, and defines the entrypoint for the application.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/gin.md#_snippet_0

LANGUAGE: Dockerfile
CODE:
```
# Use the Go 1.23 alpine official image
# https://hub.docker.com/_/golang
FROM golang:1.23-alpine

# Create and change to the app directory.
WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Copy local code to the container image.
COPY . ./

# Install project dependencies
RUN go mod download

# Build the app
RUN go build -o app
   
# Run the service on container startup.
ENTRYPOINT ["./app"]
```

----------------------------------------

TITLE: Installing Project Dependencies (Bash)
DESCRIPTION: This command is used to install or update all dependencies specified in your Clojure project's `project.clj` file. Running `lein deps` ensures that all required libraries, such as `cheshire`, are downloaded and available for your application. It's a crucial step after modifying dependencies.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/luminus.md#_snippet_3

LANGUAGE: bash
CODE:
```
lein deps
```

----------------------------------------

TITLE: Configuring Basic Axum Web Server in Rust
DESCRIPTION: This Rust code defines a minimal Axum web server. It sets up a single GET route for the root path (`/`), which responds with 'Hello World, from Axum!'. The server dynamically retrieves its listening port from the `PORT` environment variable, defaulting to `3000`, and uses `tokio` for asynchronous execution and `hyper` for serving requests.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/axum.md#_snippet_2

LANGUAGE: rust
CODE:
```
use axum::{
    routing::get,
    Router,
};

#[tokio::main]
async fn main() {
    // build our application with a single route
    let app = Router::new().route("/", get(root));

    // Get the port number from the environment, default to 3000
    let port: u16 = std::env::var("PORT")
        .unwrap_or_else(|_| "3000".to_string()) // Get the port as a string or default to "3000"
        .parse() // Parse the port string into a u16
        .expect("Failed to parse PORT");

    // Create a socket address (IPv6 binding)
    let address = SocketAddr::from(([0, 0, 0, 0, 0, 0, 0, 0], port));
    let listener = tokio::net::TcpListener::bind(&address).await.unwrap();

    // Run the app with hyper, listening on the specified address
    axum::serve(listener, app).await.unwrap();
}

// basic handler that responds with a static string
async fn root() -> &'static str {
    "Hello World, from Axum!"
}
```

----------------------------------------

TITLE: Initializing a Railway Project (Bash)
DESCRIPTION: This command initializes a new Railway project within the current Vue application directory. It guides the user through naming the project and sets up the necessary configuration for deployment to Railway.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/vue.md#_snippet_3

LANGUAGE: bash
CODE:
```
railway init
```

----------------------------------------

TITLE: Wrapping Dockerfile Start Command for Environment Variables - Shell
DESCRIPTION: This shell command demonstrates how to enable environment variable expansion for start commands in Dockerfile or image-based deployments on Railway. Since Docker's exec form does not support variable expansion directly, wrapping the command with `/bin/sh -c` allows variables like `$PORT` to be correctly interpreted before execution. This is crucial for dynamic configuration of applications.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/start-command.md#_snippet_0

LANGUAGE: shell
CODE:
```
/bin/sh -c "exec python main.py --port $PORT"
```

----------------------------------------

TITLE: Creating New Phoenix Application - Bash
DESCRIPTION: This command generates a new Phoenix application named 'helloworld_distillery'. It prompts the user to install all necessary dependencies for the project.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/phoenix-distillery.md#_snippet_1

LANGUAGE: bash
CODE:
```
mix phx.new helloworld_distillery
```

----------------------------------------

TITLE: Running an Angular Application Locally
DESCRIPTION: This command starts the Angular development server, making the application accessible locally, typically at `http://localhost:4200`. It uses the `start` script defined in `package.json` for local development.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/angular.md#_snippet_1

LANGUAGE: bash
CODE:
```
npm start
```

----------------------------------------

TITLE: Deploying FastAPI with Railway CLI
DESCRIPTION: These commands demonstrate how to initialize a new Railway project and deploy a FastAPI application using the Railway CLI. `railway init` sets up the project, and `railway up` initiates the deployment process by uploading application files.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/fastapi.md#_snippet_1

LANGUAGE: bash
CODE:
```
railway init
railway up
```

----------------------------------------

TITLE: Install AWS CDK CloudFront Packages
DESCRIPTION: Installs necessary AWS CDK packages for CloudFront, CloudFront Origins, and core utilities using npm.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/tutorials/add-a-cdn-using-cloudfront.md#_snippet_7

LANGUAGE: plaintext
CODE:
```
npm install @aws-cdk/aws-cloudfront @aws-cdk aws-cloudfront-origins @aws-cdk/core
```

----------------------------------------

TITLE: Installing pg-promise Package (Bash)
DESCRIPTION: This command uses `npm` to install the `pg-promise` library, a PostgreSQL database access layer for Node.js. It adds the package to the project's dependencies, enabling the application to interact with a PostgreSQL database.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/express.md#_snippet_2

LANGUAGE: Bash
CODE:
```
npm i pg-promise
```

----------------------------------------

TITLE: Starting Node.js Application with OpenTelemetry Instrumentation SDK
DESCRIPTION: This custom start command for a Node.js application ensures that the OpenTelemetry instrumentation SDK is loaded before the main application file (app.js). The --require ./instrumentation.js flag preloads the SDK, allowing it to wrap and instrument the application's code from startup, capturing telemetry data effectively.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/tutorials/deploy-an-otel-collector-stack.md#_snippet_8

LANGUAGE: plaintext
CODE:
```
node --require ./instrumentation.js app.js
```

----------------------------------------

TITLE: Minimal Structured Log Example (JSON)
DESCRIPTION: A basic example of a structured log in JSON format, containing only the essential `level` and `message` fields. This format is used for simple informational logs.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/logs.md#_snippet_18

LANGUAGE: json
CODE:
```
{"level":"info","message":"A minimal structured log"}
```

----------------------------------------

TITLE: Initializing Railway Project (Bash)
DESCRIPTION: Run this command within your React app's directory to initialize a new Railway project. It prompts you to name your project and links it to your Railway account. This requires the Railway CLI to be installed and authenticated.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/react.md#_snippet_3

LANGUAGE: Bash
CODE:
```
railway init
```

----------------------------------------

TITLE: Initializing a Railway Project (Bash)
DESCRIPTION: This command initializes a new Railway project within your current Symfony application directory. It guides you through naming your project and links it to your Railway account.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/symfony.md#_snippet_2

LANGUAGE: bash
CODE:
```
railway init
```

----------------------------------------

TITLE: Configuring a Dockerfile for Beego App Deployment
DESCRIPTION: This Dockerfile defines the build process for a Beego application, starting from the official Go 1.22 image. It sets up the working directory, copies the application source, downloads Go module dependencies, builds the executable, and specifies the entrypoint for running the compiled application within the container.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/beego.md#_snippet_10

LANGUAGE: Dockerfile
CODE:
```
# Use the Go 1.22 official image
# https://hub.docker.com/_/golang
FROM golang:1.22

# Create and change to the app directory.
WORKDIR /app

# Copy local code to the container image.
COPY . ./

# Install project dependencies
RUN go mod download

# Build the app
RUN go build -o app
   
# Run the service on container startup.
ENTRYPOINT ["./app"]
```

----------------------------------------

TITLE: Creating a Basic Spring Boot Web Application in Java
DESCRIPTION: This Java code defines a Spring Boot application that serves a simple 'Hello world' message. It uses `@SpringBootApplication` for auto-configuration, `@RestController` to handle web requests, and `@GetMapping("/")` to map the `hello()` method to the root URL, returning a formatted string. This setup allows the application to run as a standalone web server.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/spring-boot.md#_snippet_0

LANGUAGE: Java
CODE:
```
package com.railwayguide.helloworld;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class HelloworldApplication {

	public static void main(String[] args) {
		SpringApplication.run(HelloworldApplication.class, args);
	}

	@GetMapping("/")
    public String hello() {
      return String.format("Hello world from Java Spring Boot!");
    }

}
```

----------------------------------------

TITLE: Installing Node.js Dependencies for Express App
DESCRIPTION: This `npm` command installs the necessary Node.js packages for the Express application. It includes `express` for the web server, `winston` for logging, `winston-syslog` for syslog transport, and `dd-trace` for Datadog APM tracing, enabling the application to send logs and traces to the Datadog Agent.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/tutorials/set-up-a-datadog-agent.md#_snippet_4

LANGUAGE: npm
CODE:
```
npm i express winston winston-syslog dd-trace
```

----------------------------------------

TITLE: Opening Railway Documentation with CLI
DESCRIPTION: This command opens the official Railway documentation site in the user's default web browser, providing quick access to help and guides.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/cli-api.md#_snippet_5

LANGUAGE: txt
CODE:
```
~ railway docs --help
Open Railway Documentation in default browser

Usage: railway docs [OPTIONS]

Options:
      --json     Output in JSON format
  -h, --help     Print help
  -V, --version  Print version
```

----------------------------------------

TITLE: Initializing New Django Project - Bash
DESCRIPTION: This command uses the `django-admin` utility to create a new Django project named 'liftoff'. It sets up the basic directory structure and essential files for a Django application, including `manage.py` and the main project settings.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/django.md#_snippet_3

LANGUAGE: Bash
CODE:
```
django-admin startproject liftoff
```

----------------------------------------

TITLE: Initializing a New Railway Project (CLI)
DESCRIPTION: Displays the help output for `railway init`, which is used to create a new project directly from the command line. Users can specify a project name using the `-n` or `--name` option, and output in JSON format with `--json`.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/cli-api.md#_snippet_10

LANGUAGE: txt
CODE:
```
~ railway init --help
Create a new project

Usage: railway init [OPTIONS]

Options:
  -n, --name <NAME>  Project name
      --json         Output in JSON format
  -h, --help         Print help
  -V, --version      Print version
```

----------------------------------------

TITLE: Creating the Project Directory Structure
DESCRIPTION: This snippet illustrates the initial directory structure for the Railway project, including a root `railway-project` folder containing `agent` and `expressapi` subdirectories. This setup organizes the Datadog agent and the Node.js application components.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/tutorials/set-up-a-datadog-agent.md#_snippet_0

LANGUAGE: plaintext
CODE:
```
railway-project/
├── agent/
└── expressapi/
```

----------------------------------------

TITLE: Starting Node.js Next.js Application with Correct Port
DESCRIPTION: This bash command demonstrates how to start a Next.js application, explicitly setting the listening port using the `PORT` environment variable provided by Railway, with a fallback to 3000. This is necessary for Next.js to bind correctly and avoid "Application Failed to Respond" errors.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/reference/errors/application-failed-to-respond.md#_snippet_2

LANGUAGE: bash
CODE:
```
next start --port ${PORT-3000}
```

----------------------------------------

TITLE: Installing Database Packages for NestJS (NPM)
DESCRIPTION: This command installs the necessary Node.js packages for integrating TypeORM and PostgreSQL into a NestJS application. '@nestjs/typeorm' provides NestJS-specific integration, 'typeorm' is the ORM library, and 'pg' is the PostgreSQL database driver.

SOURCE: https://github.com/railwayapp/docs/blob/main/src/docs/guides/nest.md#_snippet_3

LANGUAGE: Bash
CODE:
```
npm i @nestjs/typeorm typeorm pg
```