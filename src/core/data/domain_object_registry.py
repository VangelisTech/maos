from typing import Dict, Type, Optional
from src.core.data.schema.base.domain_object import DomainObject, DomainObjectAccessor

class DomainObjectRegistry:
    _instance: Optional['DomainObjectRegistry'] = None
    _registry: Dict[str, Type[DomainObject]] = {}
    _accessor_registry: Dict[str, Type[DomainObjectAccessor]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DomainObjectRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, domain_object: Type[DomainObject], accessor: Type[DomainObjectAccessor]):
        object_type = domain_object.Meta.type
        cls._registry[object_type] = domain_object
        cls._accessor_registry[object_type] = accessor

    @classmethod
    def get_domain_object(cls, object_type: str) -> Optional[Type[DomainObject]]:
        return cls._registry.get(object_type)

    @classmethod
    def get_accessor(cls, object_type: str) -> Optional[Type[DomainObjectAccessor]]:
        return cls._accessor_registry.get(object_type)

    @classmethod
    def get_all_types(cls) -> List[str]:
        return list(cls._registry.keys())

    @classmethod
    def is_registered(cls, object_type: str) -> bool:
        return object_type in cls._registry

domain_registry = DomainObjectRegistry()

def register_domain_object(domain_object: Type[DomainObject], accessor: Type[DomainObjectAccessor]):
    domain_registry.register(domain_object, accessor)