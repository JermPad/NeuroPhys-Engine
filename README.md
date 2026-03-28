# NeuroPhys-Engine
A for-fun project: Trying to make a neuromorphic-inspired physics research database that stores concepts, equations, assumptions, and symbolic workflows as an activation graph for associative retrieval and reusable stability-analysis pipelines.

requirements.txt: lists python packages project deps on

data/ folder: stores the sample project data

neurophys/ folder: python package folder 
    models.py: defines data structures
    loader.py: loads json files into python objects
    engine.py: holds main logic for retrieval (and later the neuromorphic activation behavior)
    cli.py:    handles terminal commands