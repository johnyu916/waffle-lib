import json
import numpy
class SyrupEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        elif isinstance(obj, numpy.float32):
            return numpy.asscalar(obj)
        return json.JSONEncoder.default(self, obj)
