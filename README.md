# Home Assistant Sonic custom integration
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/markvader/sonic_hacs)

This is an early beta version of a custom integration for Sonic smart water shutoff valve 

It utilises the [herolabsapi python library](https://pypi.org/project/herolabsapi/) that I have
 written to interact with Sonic devices using the official Hero Labs API.

# Installation

Ideally this will be adopted as an inbuilt integration, however while development and testing are 
ongoing the recommended way to install `sonic_hacs` is through [HACS](https://hacs.xyz/).

While this is in active development and probably got a few bugs I will be keeping this within HACS as a 
custom repository and not yet available in the main HACS listing.

## To install it: 
1. Open `HACS` within `Home Assistant`
2. Go to any of the sections (`integrations`, `frontend`, `automation`).
3. Click on the 3 dots in the top right corner.
4. Select `Custom repositories`
5. Add the repository URL `https://github.com/markvader/sonic_hacs`
   and select the `integrations` category.
7. Click the `ADD` button.
8. Then `restart Home Assistant`
9. Go to `Settings` / `Devices & Services (Integrations Tab)` / `Add Integration` 
and search for `Sonic (Hero Labs)`

## Configuration

10. Log into your Hero Labs account (Email & Password).
11. The first Sonic device on your account should be discovered, 
and you can assign it to an area within your home.

## To update the integration
As development happens there will be updates to the integration, so it will be good to periodically update, 
## In HACS:
1. Click on Integrations, 
2. Scroll down and find the "Sonic (Beta) by @markvader"
3. Click the 3 dots on the lower right corner and click "Redownload"

# How you can help?
Please file issues within the [github repository](https://github.com/markvader/sonic_hacs/issues) for anything 
that you think could be broken, is broken, could be improved or is a requested feature.

