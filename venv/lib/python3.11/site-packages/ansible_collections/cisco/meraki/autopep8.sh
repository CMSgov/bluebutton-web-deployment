#!/bin/bash

# Encuentra todos los archivos .py y aplica autopep8 para formatearlos
find . -name '*.py' -exec autopep8 --in-place '{}' \;
