import ctypes
import os


def system_executable(*parts: str) -> str:
    if not parts or any(os.path.basename(part) != part for part in parts):
        raise RuntimeError("system executable path must contain plain path segments")

    buffer = ctypes.create_unicode_buffer(32768)
    length = ctypes.windll.kernel32.GetSystemDirectoryW(buffer, len(buffer))
    if length <= 0 or length >= len(buffer):
        raise RuntimeError("could not resolve the Windows system directory")

    path = os.path.join(buffer.value, *parts)
    if not os.path.isfile(path):
        raise RuntimeError(f"system executable not found: {path}")
    return path


def powershell_executable() -> str:
    return system_executable("WindowsPowerShell", "v1.0", "powershell.exe")
