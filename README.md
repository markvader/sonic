# Home Assistant Sonic custom integration
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

This is a beta version of a custom integration for Sonic smart water shutoff valve, more features are still to be added.  Additionally I am exploring local access to the sonic device to remove the need to communicate with the cloud API.

It utilises the [herolabsapi python library](https://pypi.org/project/herolabsapi/) that I have written to interact with Sonic devices using the official Hero Labs API (cloud based).

# Integration Development
[Full commit history](https://github.com/markvader/HAcore/tree/sonic-dev/homeassistant/components/sonic) 

# Installation

Ideally this will be adopted as an inbuilt integration, however while development and testing are ongoing the recommended way to install `Sonic` is through [HACS](https://hacs.xyz/).

## To install it: 
1. Open `HACS` within `Home Assistant`
2. Click the `Integrations` section, then `Explore and Download Repositories` button.
3. Search for `Sonic by markvader` then click on the `download` button
4. Select the latest version (or latest beta version) and download
5. Then `restart Home Assistant`
6. Go to `Settings` / `Devices & Services (Integrations Tab)` / `Add Integration` and search for `Sonic (Hero Labs)` then follow the configuration steps below

## Configuration

7. Log into the integration with your Hero Labs account details (Email & Password).
8. Any sonic devices on your account should be discovered, an additional device will be setup for each property registered to your account (e.g. if you have 2 properties with a sonic device at each property you will have 4 devices setup).
9. You can assign each device to an area within your home.

## To update the integration
As development happens there will be updates to the integration, so it will be good to periodically update, 
## In HACS:
1. Click on Integrations, 
2. Scroll down and find the "Sonic (Beta) by @markvader"
3. Click the 3 dots on the lower right corner and click "Redownload"

# How you can help?
Please file issues within the [github repository](https://github.com/markvader/sonic_hacs/issues) for anything that you think could be broken, is broken, could be improved or is a requested feature.

