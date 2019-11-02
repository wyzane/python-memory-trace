# @Time    : 2019/11/2 下午3:46
# @Author  : Wyzane
# @Intro   : https://www.cnblogs.com/xybaby/p/7491656.html


import datetime
import objgraph


class ObjectTrace:

    __slots__ = ("limit", "graph_type", "growth_file")

    def __init__(self, limit=8,
                 graph_type="growth",
                 growth_file=None):
        self.limit = limit
        self.graph_type = graph_type
        self.growth_file = growth_file

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = None

            if self.graph_type == "growth":
                result = self.object_trace(func, *args, **kwargs)
            return result
        return wrapper

    def object_trace(self, func, *args, **kwargs):
        """
        display the growth information of objects
        """
        start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.growth_file:
            with open(self.growth_file, "w") as file:
                file.write("start:" + start + "\n")
                objgraph.show_growth(self.limit, file=file)
                result = func(*args, **kwargs)
                objgraph.show_growth(self.limit, file=file)

                end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write("end:" + end + "\n")
        else:
            print("========object trace========")
            print("start:", start)
            objgraph.show_growth(self.limit)
            result = func(*args, **kwargs)
            objgraph.show_growth(self.limit)
            end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("end:", end)
        return result

    @staticmethod
    def object_backref(obj, max_depth=10,
                       backref_file="object_backref.dot"):
        print("========object backref========")
        trace_objects = objgraph.by_type(obj)
        try:
            objgraph.show_backrefs(trace_objects[0],
                                   max_depth,
                                   filename=backref_file)
        except IndexError:
            pass
