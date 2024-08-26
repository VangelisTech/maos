from src.core.data.domain.base import DomainObject

class BasePlugin(DomainObject):
    def initialize(self):
        pass
    def execute(self):
        pass