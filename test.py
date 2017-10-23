class A(object):
    def __setattr__(self, name, value):
        print("name:{},value:{}".format(name, value))

    def __delattr__(self, name):
        print("del {}".format(name))

    def __dir__(self):
        print("my dir")
        return ['a']

    def __eq__(self, obj):
        print("my eq")
        return obj is not None

    def __format__(self,format_spec):
        print("format_spec : {}".format(format_spec))
        return "b"
    
    def __ge__(self,value):
        #沒完成
        print("my ge")
        return value > 5

a = A()
a>3


class Test(A):
    def __ge__():
        pass

    def __getattribute__():
        pass

    def __gt__():
        pass

    def __hash__():
        pass

    def __init__():
        pass

    def __init_subclass__():
        pass

    def __le__():
        pass

    def __lt__():
        pass

    def __ne__():
        pass

    def __new__():
        pass

    def __reduce__():
        pass

    def __reduce_ex__():
        pass

    def __reduce_ex__():
        pass

    def __repr__():
        pass

    def __setattr__():
        pass

    def __sizeof__():
        pass

    def __subclasshook__():
        pass

    def __str__():
        pass

    def __call(self):

        print("call Test")
