import pathlib
from setuptools import find_packages

from requirements_checker import Packages


# =====================================================================================================================
pkgs_cli = Packages()

print()
print("1=pip========================================")
pkgs_cli.upgrade_pip()
print()
print("2=find_packages========================================")
pkgs_cli.upgrade(find_packages())
print()
print("3=upgrade__centroid457========================================")
pkgs_cli.upgrade__centroid457()
print()
print("4=requirements.txt========================================")
filepath = pathlib.Path(__file__).parent.joinpath("requirements.txt")   # FIXME: not working!
pkgs_cli.upgrade_file(filepath)


# EXIT PAUSE ==========================================================================================================
# for i in range(10, 0, -1):
#     print(f"exit in [{i}] seconds")
#     time.sleep(1)

msg = f"[FINISHED] press Enter to close"
print(msg)
print(msg)
print(msg)
print(msg)
print(msg)
# ---------
input(msg)


# =====================================================================================================================
