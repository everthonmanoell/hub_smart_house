class PotenciaWDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        if isinstance(value, int) and value >= 0:
            setattr(instance, self.private_name, value)
        else:
            raise ValueError(f"O valor: {value} tem que ser >= 0")
