# TestFlight Build App Size Chart

## About

Generate a chart of the file sizes of your TestFlight builds over time

## Example

```yml
name: Example Workflow

on: [push]

jobs:
  example_job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Generate File Size Chart
        uses: nthState/TestFlightBuildSizeChart
        with:
          ISSUER_ID: ${{ secrets.APPCONNECT_API_ISSUER }}
          KEY_ID: ${{ secrets.APPCONNECT_API_KEY_ID }}
          PRIVATE_KEY: ${{ secrets.APPCONNECT_API_KEY_PRIVATE }}
          APP_ID: id of the app
          DEVICES: "Universal iPhone15,3"
          MAX_VERSIONS: 20
          EXPORT_AS: "my_chart.png"
          

```

## Testing

### Docker

Build the docker

```bash
docker build . -t githubactiontest -f Dockerfile
```

Run the docker

```bash
docker run \
-e ISSUER_ID=appstore connect api issuer id \
-e KEY_ID=appstore connect api key id \
-e PRIVATE_KEY=appstore connect api private key  \
-e APP_ID=app id \
-e DEVICES="List of devices, separated by space, ie Universal iPhone15,3" \
-e MAX_VERSIONS=Maximum versions back to use \
-e EXPORT_AS=Export file name \
-d githubactiontest
```

### Command line

export ISSUER_ID=
export KEY_ID=
export PRIVATE_KEY=
export APP_ID=
export DEVICES="Universal iPhone15,3"
export MAX_VERSIONS=20
export EXPORT_AS="my_chart.png"
python3 ../../../main.py

### Build

Generating the requirements.txt

Create a virtual env

```bash
mkdir api_venv 
cd api_venv/                                             
python3.10 -m venv venv
cd venv/bin
source activate
```

Then install the libraries
```bash
pip3 install cryptography                                
pip3 install requests
pip3 install pyjwt
pip3 install numpy
pip3 install matplotlib
```

Export the requirements
```bash
pip3 freeze > requirements.txt 
```