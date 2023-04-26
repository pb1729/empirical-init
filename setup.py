from setuptools import setup

required_packages = [
  "torch",
]

setup(
  name="empirical_init",
  version="0.0.0",
  description="Automatically initialize weights in pytorch modules using a hacky empirical method.",
  url="https://github.com/pb1729/factor-loss/empirical-init",
  author="Phillip Bement",
  author_email="{author_first_name}{author_last_initial}@fastmail.com",
  license="BSD 3-clause",
  packages=["empirical_init"],
  install_requires=required_packages,
)

