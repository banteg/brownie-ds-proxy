from brownie import Script, accounts, history, interface

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
registry = interface.ProxyRegistry("0x4678f0a6958e4d2bc4f1baf7bc52e8f3564f3fe4")


def build_proxy(user):
    """
    Builds a proxy for user or returns the already created one.
    """
    if registry.proxies(user) == ZERO_ADDRESS:
        registry.build({"from": user})
    return interface.DSProxy(registry.proxies(user))


def cache_script(user, script):
    """
    Optionally cache the library so you can call (address,calldata) instead of (bytecode,calldata).
    """
    proxy = interface.DSProxy(registry.proxies(user))
    cache = interface.DSProxyCache(proxy.cache())
    library = cache.read(script.bytecode)
    if library == ZERO_ADDRESS:
        cache.write(script.bytecode, {"from": user})
    return script.at(cache.read(script.bytecode))


def call_proxy(user, script, data, cache=False):
    """
    Calls a stateless `script` with `data` payload.
    """
    proxy = build_proxy(user)
    if cache:
        library = cache_script(user, script)
        proxy.execute["address,bytes"](library, data, {"from": user})
    else:
        proxy.execute["bytes,bytes"](script.bytecode, data, {"from": user})


def main():
    user = accounts.load(input("account: "))
    # HACK: the address doesn't matter since we only use the contract instance to encode calldata
    script = Script.at(str(registry))

    uni = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
    data = script.seize.encode_input(uni)
    call_proxy(user, script, data)
