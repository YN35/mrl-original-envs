import minerl
import time
from minerl.env.malmo import MinecraftInstance


def main():
    """
    Tests launching and closing a Minecraft process.
    We should use the python unit test framework :O
    """
    inst = MinecraftInstance(10000)
    inst.launch(10000)
    inst = MinecraftInstance(10001)
    inst.launch(10001)
    inst = MinecraftInstance(10002)
    inst.launch(10002)
    # inst = MinecraftInstance(10003)
    # inst.launch(10003)
    # time.sleep(10)
    # inst.kill()


if __name__ == "__main__":
    main()