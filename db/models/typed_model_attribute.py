class TypedAttribute:
    def __init__(self, data_type):
        self.data_type = data_type
        self._value = None

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, self.data_type) or value == None:
            raise TypeError(f"The type must be {self.data_type}")
        self._value = value

    def __delete__(self, instance):
        self._value = None
