from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="farm2home",
	version="1.0.0",
	description="Farm-to-Home Subscription Platform connecting farmers directly with customers",
	author="Farm2Home Team",
	author_email="support@farm2home.local",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
