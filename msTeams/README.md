# Selemander - MSTeams

## Set-up:
1. Download the latest version of `chromedriver` from [this](https://sites.google.com/a/chromium.org/chromedriver/downloads) site.
2. Move the downloaded driver executable to `/opt/WebDriver/bin`.
3. Add the executable to your `$PATH`. For this:
    - In a terminal instance, type: `export PATH=$PATH:/opt/WebDriver/bin >> ~/.profile`
    - For the above change to take effect either restart your computer, or source your profile with: `source ~/.profile`
4. The webdriver should be successfully set-up by now. Proceed with the below steps to install dependencies and run the project.

## Installation:

#### Method 1:
If you have `make` installed then this is going to simple as HELL. 😈
```
# Execute all of the below commands from the root of the app, where a Makefile is present

# To setup and install the app, just type
make

# To run the app, just type
make run

# For more help, regarding other supported make commands, type
make help
```

#### Method 2:
Even if method 1 doesn't works for you, this is going to be simple as HEAVEN...Trust me!! 🌠
```
# Setup your venv and activate it.
python3 -m venv <your-venv-name>
source <your-venv-name>/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Run the app with
python app.py
```

Enjoy!!! :fire: :fire:

If you face in issue/bug or difficulty in setup/installation, feel free to raise an issue :book:.
