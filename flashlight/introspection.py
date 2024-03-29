import numpy as np
import torch

import composit as cnp
import composit.nn
from composit.string import random_string
import flashlight


def convert_torch_tensors_to_lazy_tensors(*args, allow_scalars=False):
    first_arg = None
    for index, arg in enumerate(args):
        if isinstance(arg, flashlight.Tensor):
            result = arg.lazy_tensor
        elif isinstance(arg, torch.nn.parameter.Parameter):
            np_tensor = arg.detach().numpy()
            result = cnp.asarray(np_tensor)
        elif isinstance(arg, torch.Tensor):
            np_tensor = arg.detach().numpy()
            result = cnp.nn.variable(name=random_string(), shape=np_tensor.shape, dtype=np_tensor.dtype)
            arg.lazy_tensor = result
        elif allow_scalars and isinstance(arg, (int, float)):
            result = cnp.asarray(
                np.asarray(arg, first_arg.dtype), name=f"scalar_{arg}")
        else:
            continue

        if index == 0:
            first_arg = result

        yield result
