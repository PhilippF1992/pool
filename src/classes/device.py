class Device(dict):
    def __init__(self, identifiers, name, sw_version, model, manufacturer):
        super().__init__()
        self.name = name
        self["identifiers"] = identifiers
        self["name"] = name
        self["sw_version"] = sw_version
        self["model"] = model
        self["manufacturer"] = manufacturer