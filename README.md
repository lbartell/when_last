When Last
=====


App for tracking _When Did I Last?_ do a task

# Developer instructions

## BeeWare
This app is developed using [BeeWare](https://docs.beeware.org/en/latest/index.html),
with `toga` ([docs](https://toga.readthedocs.io/en/latest/index.html)) for GUI and 
`briefcase` ([docs](https://briefcase.readthedocs.io/en/latest/)) for package management.

## Env setup
- Python 3.9 environment via `direnv`
- Install dependencies: `pip install -r requirements.txt`

## `Briefcase` usage

All commands from the `when_last` directory

- Start project in developer mode: `briefcase dev`
- Package for distribution (first time or when dependencies chnage)
    1. Create config scaffolding: `briefcase create`
    1. Compile application: `briefcase build`
    1. [MacOS] Add permissions to run app: `codesign --force --deep --sign - "macOS/app/When Last/When Last.app"`
    1. Run compiled app: `briefcase run`
- Update previously-build package: `briefcase update`
- Build installer: `briefcase package --no-sign`
