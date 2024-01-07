class B():
    def b():
        print("hi")
    def a(self):
        staticmethod(getattr(self, "b"))()
        


B().a()
