import sys
import platform
print(f"\nsys.version:\n{sys.version}")
print(f"\nsys.version_info:\n{sys.version_info}")

print(f"\nplatform.python_version():\n{platform.python_version()}")
print(f"\nplatform.architecture():\n{platform.architecture()}")
print(f"\nplatform.machine():\n{platform.machine()}")
print(f"\nplatform.platform():\n{platform.platform()}")
print(f"\nplatform.processor():\n{platform.processor()}")
print(f"\nplatform.python_compiler():\n{platform.python_compiler()}")
print(f"\nplatform.python_implementation():\n{platform.python_implementation()}")
print(f"\nplatform.system():\n{platform.system()}")
print(f"\nplatform.mac_ver():\n{platform.mac_ver()}")
print(f"\nplatform.libc_ver():\n{platform.libc_ver()}")

