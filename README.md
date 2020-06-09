# Prometheus Recording Rule Generator
A project to simplify generating recording rules that can be used to filter in alerting rules.

[![Build Status](https://cloud.drone.io/api/badges/wbh1/prometheus_rule_overrider/status.svg)](https://cloud.drone.io/wbh1/prometheus_rule_overrider)

## Use Case
This was born out of a need to apply "Global" alerts to *almost* all scrape targets, but exclude a few for various reasons (e.g. don't alert for disk usage on a drive solely dedicated to pagefile usage).

This exclusion is done by leveraging the the `unless` operator in PromQL [(docs here)](https://prometheus.io/docs/prometheus/latest/querying/operators/#logical-set-binary-operators). However, because the `unless` operator requires every label on the right side of the expression to match to the left side, it can make adding these "overrides" pretty tedious. 

I wanted to create an easy way to programatically add recording rules and thus this project was born. Now, if an alert fires off and you want to add an override for it, you need only to copy and paste the label set from the Prometheus web UI into this YAML-based configuration file and then you can generate the new overrides file. 

## Usage
*NOTE: the files in the directory specifying your overrides MUST end in `.yml` because I am just that awful and opinionated of a person.*

```
❯ python generate.py --help
usage: generate.py [-h] [--dest DEST] [--stdout] dir

positional arguments:
  dir          Directory containing .yml files with overrides

optional arguments:
  -h, --help   show this help message and exit
  --dest DEST  Destination to write out the file containing recording rules
  --stdout     Write YAML to STDOUT instead of a file (takes precedence over --dest)
```

You can reference the `testdata/global.yml` file for how the overrides file(s) should be formatted.

## Recommendations
- Take care when naming your overrides input files - the filename is used to name the recording rule group. For example. `global.yml` becomes `Override_Global` and `linux.yml` would become `Override_Linux`.

- Use CI/CD to generate the recording rules programatically. A Dockerfile is provided if you wish to build your own image, or you can use the one available from Dockerhub at [wbh1/prom_rule_overrider](https://hub.docker.com/repository/docker/wbh1/prom_rule_overrider/general).

## Future
This project could be easily extended to be used to programatically generate recording rules in general, but I have not implemented such functionality since I currently have no need for it. 

If you would find this functionality useful, let me know!