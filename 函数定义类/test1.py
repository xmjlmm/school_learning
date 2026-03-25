def extend(father_class):
    def decorator(current_class):
        class DecoratedClass:
            def __init__(self, *args, **kwargs):
                if father_class is None:
                    self_instance = current_class(lambda: ..., *args, **kwargs)
                else:
                    super_object = father_class(*args, **kwargs)
                    self_instance = current_class(super_object, *args, **kwargs)

                # Copy attributes from self_instance to DecoratedClass instance
                self.__dict__.update(self_instance.__dict__)

        return DecoratedClass

    return decorator


@extend(None)
def Animal(self, *args, **kwargs):
    self.name = kwargs.get('name', 'Unknown')

    def to_string():
        return f"I am {self.name} and I am an animal."

    self.to_string = to_string
    return self


@extend(Animal)
def Dog(self, *args, **kwargs):
    self.age = kwargs.get('age', 10)
    self.super_to_string = self.to_string

    def to_string():
        print(self.super_to_string())
        return f"I am {self.name} and I am {self.age} years old."

    self.to_string = to_string
    return self

def main():
    dog = Dog(name='Max', age=5)
    print(dog.to_string())

if __name__ == '__main__':
    main()


