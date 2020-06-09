import glob

from .models import RecordingRuleGroup, RecordingRule
from ruamel.yaml import YAML


class Overrider:
    def __init__(self, overrides_dir):
        self.__yamlsetup__()
        self.override_files = glob.glob(f"{overrides_dir}/*.yml")
        self.overrides_dir = overrides_dir
        self.output = {"groups": []}

    def __yamlsetup__(self):
        yaml = YAML(typ="unsafe")

        # Set this to output dictionary on multiple lines
        yaml.default_flow_style = False

        # These next few lines are required in order to NOT output a YAML tag when
        # serializing Python objects (e.g. !!python/object:__main__.RuleOverride)
        yaml.representer.org_represent_mapping = yaml.representer.represent_mapping

        def custom_represent_mapping(tag, mapping, flow_style=None):
            if tag.startswith("tag:yaml.org,2002:python/object"):
                tag = "tag:yaml.org,2002:map"
            return yaml.representer.org_represent_mapping(
                tag, mapping, flow_style=flow_style
            )

        yaml.representer.represent_mapping = custom_represent_mapping

        self.yaml = yaml

    def process(self):
        yaml = self.yaml
        for _f in self.override_files:
            # Create a group name for the resulting rule file by prefixing
            # with "Override_" plus a capitalized version of the filename
            # after stripping out the file extension
            GROUP_NAME = (
                "Override_"
                + _f.split(f"{self.overrides_dir}/")[1].split(".yml")[0].capitalize()
            )
            rule_group = RecordingRuleGroup(GROUP_NAME)

            with open(_f) as f:
                # Adapt Prometheus's label key/value syntax to YAML's K/V syntax
                contents = f.read().replace("=", ": ")

                overrides = yaml.load(contents)

                for alert in overrides:
                    RULE_NAME = "override:" + alert["alertname"]

                    for labelset in alert["overrides"]:
                        _override = RecordingRule(RULE_NAME, labelset)
                        rule_group.add(_override)

            self.output["groups"].append(rule_group)

    def dump(self, dest):
        self.yaml.dump(self.output, dest)
