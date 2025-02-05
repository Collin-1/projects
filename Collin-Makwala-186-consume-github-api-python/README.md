# Consume GitHub API 

This project provides a Python script to use the GitHub API. It retrieves pull requests from a specified repository within a given date range.

## Project Structure

```
Collin-Makwala-186-consume-github-api-python/
    ├── requirements.txt
    ├── src
    |   └── consume_github_api.py
    └── setup.py
```

## Requirements

- A GitHub personal access token for authenticated requests (optional)

## Getting your own personal access token (Optional)

1. Sign in to your GitHub account.

2. Click on your profile photo in the upper-right corner of any page, then click on `Settings`.

3. In the left sidebar, click on `Developer settings`.

4. In the left sidebar, click on `Personal access tokens`.

5. Click on `Generate new token`.

6. Give your token a descriptive name.

7. Select the scopes (permissions) you'd like to grant this token. If you're unsure what scopes to select, check the documentation for the API you plan to use the token with.

8. Click `Generate token`.

9. After generating the token, make sure to copy it. You won't be able to see it again!

To use this token in your script, you need to set it as an environment variable named `GITHUB_TOKEN`. Here's how you can do that:

- On Unix/Linux/macOS:
  - Open Terminal.
  - Run `export GITHUB_TOKEN=your_token`, replacing `your_token` with the token you copied earlier.
  - Now, every time you run your Python script from this terminal session, it will have access to the `GITHUB_TOKEN` environment variable.

- On Windows:
  - Open Command Prompt.
  - Run `set GITHUB_TOKEN=your_token`, replacing `your_token` with the token you copied earlier.
  - Now, every time you run your Python script from this command prompt session, it will have access to the `GITHUB_TOKEN` environment variable.


## Installation

1. Clone this repository:
```
   git clone https://github.com/Collin-1/projects.git
```

2. Navigate to the project directory by using the following command in the virtual environment Command Terminal or Windows Terminal:
```
cd projects/Collin-Makwala-186-consume-github-api-python/
```


## Environment Setup:
1. Use the following command in the Terminal to create a virtual environment:
 ```
 python -m venv <virtual_environment_name>
 ```
2. Activate the new virtual environment that you just created using the following command:
 ```
 source <virtual_environment_name>/bin/activate   # for Unix/Linux

 .\<virtual_environment_name>\Scripts\activate    # for Windows  
 ```

3. Install the required packages:
```
pip install -r requirements.txt
```
```
pip install -e .
```


## Usage

The main script is `consume_github_api.py` located in the `src` directory. This script retrieves pull requests from a specified GitHub repository within a given date range.

Start the Python interactive shell by typing python and import the necessary functions from the module:

`from src.consume_github_api import get_pull_requests`

Then, call the get_pull_requests function with the required parameters. For example:

`get_pull_requests("Umuzi-org", "ACN-syllabus", "2022-03-01", "2022-03-10")`

Before running the script, you can optionally set the `GITHUB_TOKEN` environment variable to your GitHub personal access token to increase the rate limit of your requests:
