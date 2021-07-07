from neads.plugin import Plugin, PluginID

built_in_max = max
built_in_min = min
built_in_pow = pow


def _const(a):
    return a


def _add(a, b):
    return a + b


def _sub(a, b):
    return a - b


def _mul(a, b):
    return a * b


def _div(a, b):
    return a / b


def _max(*args):
    return built_in_max(*args)


def _min(*args):
    return built_in_min(*args)


def _pow(x, base=2):
    return base**x


def _factor(n):
    """Return ordered list primes which divide the given number n."""
    sieve = [True] * n
    sieve[0] = False
    factors = []
    idx = 1
    while idx < len(sieve):
        if sieve[idx]:
            examined = idx + 1
            if not n % examined:
                factors.append(examined)
                for remove_idx in range(idx + examined, len(sieve), examined):
                    sieve[remove_idx] = False
        idx += 1
    return factors


const = Plugin(PluginID('const', 0), _const)
add = Plugin(PluginID('add', 0), _add)
sub = Plugin(PluginID('sub', 0), _sub)
mul = Plugin(PluginID('mul', 0), _mul)
div = Plugin(PluginID('div', 0), _div)
max = Plugin(PluginID('max', 0), _max)
min = Plugin(PluginID('min', 0), _min)
pow = Plugin(PluginID('pow', 0), _pow)
factor = Plugin(PluginID('factor', 0), _factor)
