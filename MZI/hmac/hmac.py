b = 256
opad = bytes((x ^ 0x5C) for x in range(b))
ipad = bytes((x ^ 0x36) for x in range(b))


class Hmac:
    def __init__(self, key, message, digest):
        self.key = key
        self.message = message
        self.digest = digest

    def use(self):
        inner = self.digest()
        outer = self.digest()
        if len(self.key) > inner.block_size:
            self.key = self.digest(self.key).digest()
        self.key = self.key.ljust(inner.block_size, b'\x00')

        inner.update(self.key.translate(ipad))
        inner.update(self.message)

        outer.update(self.key.translate(opad))
        outer.update(inner.digest())
        return outer.digest()
