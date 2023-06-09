# Empirical Init

This package provides a way of automatically initializing weights in pytorch neural networks using a hacky empirical method. Why do we need it? Well, there are other ways of normalizing weights. But batch norm is terrible, and layer norm is a non-linearity, which is kind of funky. Also, we not only need to keep activations from diverging, we need to keep the gradients from diverging too, and it would be *really* funky to apply a non-linearity to our gradients. The [maximum update parametrization](http://proceedings.mlr.press/v139/yang21c/yang21c.pdf) of Greg Yang and Edward Hu provides a recipe for how to scale all the gradients and activations so that the following three pillars are upheld:

* Non-divergent activations: Activations in all layers should be approximately O(1)
* Non-divergent gradients: Gradients in all layers should be approximately O(1)
* Maximum stable update: The change in activations for learning rate equal to 1 should be approximately O(1). (But in practice we don't want updates quite this large so we'll use a smaller learning rate like `1e-3` or something.)

Their technique for achieving this is to represent the neural network as a tensor program and then do a whole lot of math to figure out how the activations and gradients and updates will flow through the network. But all that sounds like *work*. Know what's easier and no work at all? Just running your neural network! You already have it coded up, running it is a single function call. Then instead of *computing* all these things, we can just *measure* them.

## Usage

Empirical init works by wrapping all modules in a helper module that scales the activations and gradients by tunable amounts. The wrapper class is called `Normed`, and you can certainly wrap your submodules manually. But the easiest way to wrap all submodules is to use the decorator `@wrap_all_leaf_modules` to modify `__init__()`. This will wrap every leaf module under your module that has any trainable parameters.

```
import torch.nn as nn
from empirical_init import wrap_all_leaf_modules

...

class MyModule(nn.Module):
  @wrap_all_leaf_modules
  def __init__(self, device="cpu"):
    super().__init__()
    ...
```

`Normed` has the tunable scalings registered as buffers, so they won't count as trainable but they'll still be in the state dict when you go to save your module. However, these scalings must actually be tuned to the correct values. This can be done with a call to `empirical_init` like so:

```
import torch
from empirical_init import get_wrapped_submodules, empirical_init

...

def dummy_input(batchsz):
  return torch.randn(batchsz, 100)
def dummy_loss(model_output):
  return model_output.mean()

my_module = MyModule()
empirical_init(
  get_wrapped_submodules(my_module), my_module,
  dummy_input, dummy_loss)
```

This will print out a bunch of helpful debug information about the tuning process. In particular, the magnitudes of activations and gradients going in and out of each wrapped submodule will be printed. After the call completes, all the scaling factors should be properly tuned.

Note that the number of calls made by empirical_init to your network scales with the number of layers in your network. So if your network takes a while to run or it has a lot of layers, empirical_init could take a while to terminate. Try it on a small fast network first if it's your first time using this package.

The dummy functions are there to provide realistic-looking data and gradients for your network to consume. The dummy input function should generate random input data of the provided batch size. The dummy loss function should produce a loss when passed the output of the network. A good rule of thumb is to have the dummy input function call `torch.randn()` to produce input of the right shape, and the dummy loss function should be the same as your actual loss function, but with randomized labels.
