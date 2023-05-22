#!/bin/bash

# Clonar el repositorio
git clone https://github.com/esyepesv/ASG-st0263.git

# Instalar grpcio-tools
pip install grpcio-tools

# Instalar google para python
pip install google

# Ejecutar el archivo main.py
cd /home/ubuntu/ASG-st0263/Instance/MonitorC1
python main.py
