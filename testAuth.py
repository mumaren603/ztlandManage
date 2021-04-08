def auth(func):
    def warp(*args,**kwargs):
        print("我是原先代码")
        ret = func()
        return ret
    return warp

@auth
def app01():
    print("11111")

@auth
def app02():
    print("22222")


app01()
app02()