#%%
print("This is a test.")

#%%
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

#%%
dog1 = Dog("Tom", 4)
dog2 = Dog("Phil", 3)

#%%
def get_max_age(*args):
    print(type(args))
    print(max(args))

#%%
get_max_age(dog1.age, dog2.age)

#%%
