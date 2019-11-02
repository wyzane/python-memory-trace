# @Time    : 2019/11/2 下午1:54
# @Author  : Wyzane
# @Intro   :


from MemoryTrace.object_trace import ObjectTrace


seq = list()


class Test(object):
    pass


@ObjectTrace()
def func():
    o = Test()
    seq.append(o)
    return
    seq.remove(o)


if __name__ == '__main__':
    func()
    ObjectTrace.object_backref("Test")
