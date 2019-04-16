class Test(object):
    def __init__(self, a):
        print('one', a)

        self.a = a
        print('two', self.a)

    def printA(self):
        print('three', self.a)


obj = Test(7)

obj.printA()
print('four', obj.a)
