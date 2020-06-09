class RecordingRule:

    def __init__(self, rule_name: str, labels: dict, expr="1"):
        self.record = rule_name
        self.labels = labels
        self.expr = expr


class RecordingRuleGroup:

    def __init__(self, groupname: str):
        """Create a group of recording rules to be logically grouped together
           when the YAML is dumped out to be consumed by Prometheus.

        Args:
            groupname (str): Name to give the group of rules
        """
        self.name = groupname
        self.rules = []

    def add(self, rule):
        """Add a rule override (i.e. a recording rule) to the group.

        Args:
            rule (RecordingRule): An instance of the RecordingRule class
        """
        self.rules.append(rule)
