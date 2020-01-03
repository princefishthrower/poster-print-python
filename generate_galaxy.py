import ruamel.yaml as yaml

with open("galaxies/galaxy1.yaml") as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)