from pkg_resources import NullProvider


class TestClass:
    def TestFunction(self):
        print('TestFunction')


print('hello world!!')
test = NullProvider()

print(dir(test))
file = getattr(test, '__file__', '')
print(file)
