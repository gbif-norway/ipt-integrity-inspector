# ipt-integrity-inspector
[![Run IPT Inspector](https://github.com/gbif-norway/ipt-integrity-inspector/actions/workflows/run_inspector.yml/badge.svg)](https://github.com/gbif-norway/ipt-integrity-inspector/actions/workflows/run_inspector.yml)

## Introduction

The IPT Integrity Inspector is a specialized tool designed to ensure the integrity of data published on the Integrated Publishing Toolkit (IPT) and its proper ingestion by the Global Biodiversity Information Facility (GBIF). Leveraging Python and Luigi for task automation, it checks for discrepancies or errors in data transmission and notifies the team via Discord if any issues are detected. This tool is crucial for maintaining the accuracy and reliability of biodiversity data shared across platforms.
Features

- Automated Data Verification: Automatically checks data published on multiple IPT servers for proper ingestion by GBIF.
- Error Notification: Sends alerts through Discord using webhooks for immediate awareness of any ingestion issues.
- Flexible Deployment: Can be run as a GitHub Cron Action for continuous integration or locally using Docker for isolated environments.
- Configurable: Supports customization through environment variables and a JSON configuration for IPT servers.

## Prerequisites

- Docker installed on your local machine for Docker deployment.
- GitHub account for GitHub Actions deployment.
- Discord account and a created webhook URL for error notifications.

## Installation
### Docker

To run IPT Integrity Inspector using Docker, first pull the latest image from Docker Hub:

```sh
docker pull gbifnorway/ipt-integrity-inspector:latest
```

Then run the container with the necessary environment variables:

```sh
docker run -e DISCORD_WEBHOOK=<your_discord_webhook> -e SETTINGS=<your_settings_json> gbifnorway/ipt-integrity-inspector:latest
```
### GitHub Actions

For GitHub Actions deployment, add the following secret to your repository:

- DISCORD_WEBHOOK: Your Discord webhook URL for notifications.

And following repository variable

- SETTINGS: Your JSON configuration for IPT servers, with escape characters.

The action can be configured to run on a schedule using GitHub's cron syntax within your workflow file.
## Usage
### Environment Variables

- DISCORD_WEBHOOK: The Discord webhook URL for sending notifications upon encountering errors.
- SETTINGS: A JSON string that specifies the IPT servers to check. It should be formatted with escape characters as shown below:

```json
"{\"ipt_servers\": [\"https://yout-ipt-url.com\", \"https://another-ipt.com\", ...]}"
```
> **_NOTE:_** Don't forget to use outside quotation in GitHub variables

## Contributing

Contributions to the IPT Integrity Inspector are welcome! If you'd like to contribute, please fork the repository and create a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.
