from setuptools import setup, find_packages
import os

setup(
    name='vsce_tui',
    version='0.1.0',  # Start with a version number
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here (e.g., 'requests', if you used it)
    ],
    entry_points={
        'console_scripts': [
            'vsce_tui=vsce_tui.cli:main',  # This makes it runnable from the command line
        ],
    },
    # Metadata for PyPI
    author='Your Name',
    author_email='your.email@example.com',
    description='A TUI tool for managing VS Code extensions.',
    long_description=open('README.md').read() if os.path.exists('README.md') else "", # It's good to have a README.md
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/vsce_tui',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose a license
        'Operating System :: POSIX :: Linux', # Since it's Linux-focused for now
    ],
)