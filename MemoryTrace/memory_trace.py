# @Time    : 2019/11/1 下午9:32
# @Author  : Wyzane
# @Intro   : tracemalloc模块功能
"""
1.跟踪对象的内存分配
2.统计每个文件中已分配block信息，包括：行号、占用内存总大小、
  blocks数量、每个blocks平均占用内存大小
3.比较两个snapshot之间的不同，以便定位内存泄露问题
"""


import tracemalloc


class MemoryTrace:

    def __init__(self, frame=1, mem_top=10, key_type="lineno"):
        self.frame = frame
        self.mem_top = mem_top
        self.key_type = key_type
        self.mapping_key_type = {
            "lineno": self.lineno,
            "traceback": self.traceback,
            "deference": self.deference,
        }

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = (self.mapping_key_type
                      .get(self.key_type)
                      (func, *args, **kwargs))

            self.end()

            return result

        return wrapper

    def lineno(self, func, *args, **kwargs):
        """
        display the files that most top memory was allocated
        """
        print("========lineno=======")
        tracemalloc.start()
        result = func(*args, **kwargs)
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics("lineno")

        for top in top_stats[0:self.mem_top]:
            print("mem-trace ", top)

        return result

    def traceback(self, func, *args, **kwargs):
        """
        display the traceback of the biggest memory block
        """
        print("========traceback=======")
        tracemalloc.start(self.frame)
        result = func(*args, **kwargs)
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics("traceback")
        top_one = top_stats[0]

        print("blocks count: %s" % top_one.count)
        print("size: %.1f KiB" % (top_one.size / 1024))
        for top in top_one.traceback.format():
            print("mem-trace ", top)

        return result

    def deference(self, func, *args, **kwargs):
        """
        compute the deference between two snapshot
        """
        tracemalloc.start(self.frame)
        snapshot_start = tracemalloc.take_snapshot()
        result = func(*args, **kwargs)
        snapshot_end = tracemalloc.take_snapshot()
        top_stats = snapshot_end.compare_to(snapshot_start, "lineno")

        for top in top_stats[:self.mem_top]:
            print("mem-trace ", top)

        return result

    def end(self):
        trace_malloc_module_usage = tracemalloc.get_tracemalloc_memory()
        print("trace alloc module use memory: %.1f KiB" %
              (trace_malloc_module_usage / 1024))

        current_size, peak_size = tracemalloc.get_traced_memory()
        print("current size: %.1f KiB" % (current_size / 1024))
        print("peak size: %.1f KiB" % (peak_size / 1024))

    def write(self, snapshot, filename):
        pass
