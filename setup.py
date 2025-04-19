from setuptools import setup, find_packages

setup(
    name="aws-unused-tracker",
    version="1.0.0",
    description="CLI tool to track and report unused AWS resources like EC2, EBS, and ELB",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "tabulate"
    ],
    entry_points={
        "console_scripts": [
            "aws-unused-tracker=aws_unused_tracker.cli:cli"
        ]
    },
    python_requires=">=3.6"
)

