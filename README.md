# Home Assistant Dashboard Generator

This project is a local build pipeline that dynamically generates Home Assistant YAML dashboards. Instead of manually updating the dashboard every time a new smart device is added, this tool fetches the live state of your home via the Home Assistant API and compiles a modern "Sections" dashboard using Jinja2 templates.

## Features

* **Automated Data Fetching:** Uses the Home Assistant Template API to automatically discover areas and the lights within them.
* **Jinja2 Templating:** Uses `makejinja` to compile logic-heavy templates into clean, static YAML that Home Assistant loves.
* **One-Command Deployment:** Uses `make deploy` to generate the dashboard and instantly push it to the Home Assistant server via `rsync`.
* **Secure:** Keeps all sensitive URLs and access tokens locally in a `.env` file.

---

## Requirements

To run this deployment pipeline, you need specific configurations on both your local development machine and your Home Assistant server.

### Local Machine (Your Mac/PC)

* **Python 3.x:** To run the API fetching scripts and virtual environment.
* **Make:** To run the `Makefile` commands (pre-installed on macOS/Linux).
* **rsync:** To synchronize the generated files to the server (pre-installed on macOS/Linux).

### Home Assistant Server

* **Long-Lived Access Token:** Needed to securely query your devices. Generate one by going to your Home Assistant UI: *Profile (bottom left) -> Security -> Long-Lived Access Tokens*.
* **Advanced SSH & Web Terminal Add-on:** The standard Home Assistant OS does not include `rsync` out of the box. You must use the community SSH add-on to accept the files.

---

## Home Assistant Configuration (Enabling rsync)

If you are running Home Assistant OS, you must install `rsync` on the server so your local machine can talk to it during deployment.

1. Enable **Advanced Mode** in your Home Assistant user profile.
2. Go to **Settings -> Add-ons -> Add-on Store**.
3. Install the **Advanced SSH & Web Terminal** add-on (from the Community Add-ons repository, *not* the official core "Terminal & SSH").
4. Go to the add-on's **Configuration** tab.
5. In the `packages` section, add `rsync` so it looks like this:

    ```yaml
    packages:
        - rsync
    ```

6. Set up your SSH credentials (username/password or authorized keys) in the configuration.
7. **Start/Restart** the add-on.

## Local Installation & Setup

1. Clone the repository and navigate into the folder:

    ```Bash
    git clone <your-repo-url>
    cd ha_dashboards
    ```

2. Run the setup command:

    This will automatically create an isolated Python virtual environment (`.venv`) and install all required dependencies.

    ```Bash
    make setup
    ```

3. Activate the virtual environment:
    
    You must run this command every time you open a new terminal session to work on this project.

    ```Bash
    source .venv/bin/activate
    ```

4. Configure your environment variables:

    Create a file named `.env` in the root of the project. Do not commit this file to Git. Add your specific details:

    ```Bash
    # Home Assistant API Credentials
    HA_URL=http://homeassistant.local:8123
    HA_TOKEN=your_long_lived_access_token_here

    # SSH Deployment Details
    HA_SSH_USER=root
    HA_SSH_HOST=your_ha_ip_or_domain
    HA_DASHBOARD_PATH=/config/configuration/dashboards/auto-dashboard
    ```

## Managing Python Libraries

If you decide to expand your Python scripts and need to install new libraries (e.g., `pip install beautifulsoup4`), you must update the     `requirements.txt` file. If you don't, the pipeline will break for anyone else cloning the repository (or for you on a new machine).

To safely lock in your new dependencies, just run:

```Bash
make freeze
```

This will automatically overwrite `requirements.txt` with your exact, updated environment. **Always commit the updated `requirements.txt` to version control.**

## Usage
Ensure your virtual environment is active, then run any of the following `make` commands:

### `make generate`

The core command. It runs a two-step process:

1. Executes `scripts/fetch_ha_data.py` to pull live data from HA and save it as `build/data.yaml`.

2. Runs `makejinja` to merge the data with the templates, outputting the final dashboard files into the `build/dashboards/` folder.

### `make deploy`

The deployment pipeline. It runs the `generate` process above, and then securely synchronizes the compiled YAML files directly to your Home Assistant server using `rsync`.

### `make clean`

A utility command that deletes the `build/` directory so you can start from a totally clean slate.

### `make freeze`

Updates the `requirements.txt` file with any new Python libraries you have installed in your active virtual environment.

## Project Structure

```tree
ha_dashboard_generator/
├── .env                     # Secrets
├── .env.example             # Example secrets file
|-- .envrc                   # Automatically loads .venv when you `cd` into the folder (optional)
├── .gitignore               # Git ignore rules
├── Makefile                 # Task runner commands
├── makejinja.toml           # Build tool configuration
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── scripts/                 # Any Python logic used to build the project
├── queries/                 # Jinja scripts sent to Home Assistant's API
├── templates/               # Your dashboard UI source code
└── build/                   # ALL auto-generated files go here (Ignored by Git)
    ├── data.yaml            # The intermediate fetched state
    └── dashboards/          # The final YAML ready for Home Assistant
```