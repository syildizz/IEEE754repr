#!/usr/bin/env python3

from setuptools import setup, Extension

setup(
    ext_modules = [
        Extension(
                name="ieee754repr.pfloat",
                sources=["src/ieee754repr/pfloat/pfloat.c", "src/ieee754repr/pfloat/bind.c"],
                include_dirs=["src/ieee754repr/pfloat/"]
            )
       ]
)
