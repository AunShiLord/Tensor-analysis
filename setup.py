# tensor-analysis setup.py
# from distutils.core import setup
from setuptools import setup
setup(
    name = "tensor-analysis",
    packages = ["tensor_analysis", "tensor_analysis/tests"],
    version = "0.9.3",   
    description = "Tensor analysis package for n-dimensional tensor calculation",
    author = "Vladimir Kuzmin, Konovalenko Anastasia, Merzlyakova Ksenia",
    author_email = "aunshilord@yahoo.com",
    url = "https://github.com/AunShiLord/Tensor-analysis.git",
    keywords = ["tensor", "tensor_fields", "riemannian", "arraypy", "sympy",\
                "tensor_algebra"],
    install_requires = ["sympy"], 
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",       
        ],
    long_description = """\
    Tensor analysis package.
    This is a separate version of what_we_commited_to_sympy.
    Consists of:
    Arraypy class - N-dimentional arrays.
    TensorArray class - N-dimentional array with contravariant and covariant indicies.
    Classes declared in arraypy.py file.
    
    There is also modules:
    1) tensor_methods.py       - Tensor algebra.
    2) tensor_fields.py        - operation in tensor fields like diff, rot, lie, etc...
    3) riemannian_geometry.py  - tensor operations about some riemannian geometry, ok?
    4) helper_functions.py     - some help functions.
    """
)