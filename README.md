# MHacks 24

## Introduction

This project is cool.

## Usage

1. Install [Docker](https://www.docker.com/products/docker-desktop/)
2. Add the following `.env` file inside `/api`:

   ``` sh
   env="prod"  # prod | stage | dev
   ```

3. Add an empty `.env` file inside `/web`
4. Compose up `docker-compose.yaml`

That's it! Go to [localhost:3000](localhost:3000) to use the interactive webapp, or [localhost:8000](localhost:8000) to try out the API.

## Development

1. Install [Docker](https://www.docker.com/products/docker-desktop/)
2. Add the following `.env` file inside `/api`:

   ``` sh
   env="dev"  # prod | stage | dev
   ```

3. Add an empty `.env` file inside `/web`
4. To enable linting inside your preferred IDE, create a [Python virtual environment](https://docs.python.org/3/library/venv.html) and install the Python dependencies. Likewise, install the JavaScript dependencies for JS linting.

    ``` sh
    python -m venv venv
    source venv/bin/activate  # for unix
    ./venv/Scripts/activate  # for windows
    python -m pip install -r api/requirements.txt

    cd app
    npm install yarn
    yarn install
    ```

5. Compose up `docker-compose-dev.yaml` for a build with hot-reloading enabled on the webapp upon file changes

### Testing

There are several tests scripts which can be called with the `pytest` command inside the api container. Reference the [Pytest usage guide](https://docs.pytest.org/en/6.2.x/usage.html) more details on running a specific test. For local usage, it is recommended to add the [-v flag](https://docs.pytest.org/en/stable/how-to/output.html) for verbose outputs.
