# pyrepoman

# Brief

**pyrepoman** is a python application used to perform Git actions on local Git repos (e.g. Git server provided on a Linux platform), and web host Git repos.

## Description

**py_indeed.py** is the script that does majority of the work. It is currently configured to use a headless browser to:
 * Login in to Indeed
 * Iterate over each page pulling jobs to apply for
 * Parse for jobs that can be applied for using an Indeed resume
 * Attempts to apply to each job
    - Each job could have supplement questions, the questions that the script cannot answer are stored into a database file
 * Continues to until the end of the page, goes to the next page and repeats

**py_answer.py** is the script to use for interfacing with questions pulled from py_indeed.

## Usage

## Installation

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## NOTES TO ADD LATER

# Linux Git Server Requirements

    # OPENSSH SERVER, FIREWALL SHOULD ALLOW PORT 22, SSHD SHOULD BE ON
    # GIT SHOULD BE INSTALLED
    # PYTHON 3 SHOULD BE INSTALLED
    # PUBLIC KEY AUTHENTICATION ENABLED AND SET (KEYS ARE IN THE PROPER PLACE, WITH CORRECT PERMISSIONS), PASSWORD AUTH DISABLED
    # ENDS FOR LINUX

# LINUX PATH SHOULD BE LIKE /usr/local/... default behavior is the same

