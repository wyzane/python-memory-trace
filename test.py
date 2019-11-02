# @Time    : 2019/11/1 下午9:19
# @Author  : Wyzane
# @Intro   :


from MemoryTrace.memory_trace import MemoryTrace


@MemoryTrace(frame=20, key_type="lineno")
def func():
    d = [dict(zip('xy', (0, 1))) for i in range(1000000)]
    t = [tuple(zip('xy', (0, 1))) for i in range(1000000)]


if __name__ == '__main__':
    func()
