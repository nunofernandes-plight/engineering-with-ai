# Base image from the OpenFOAM foundation or similar
FROM opencfd/openfoam-default:2306

# Switch to root to install dependencies
USER root

# Install Python and the "Shim" dependencies
# - Jinja2: For templating OpenFOAM dictionaries
# - NumPy: For handling data arrays
# - PyVista: For reading VTK/OpenFOAM results without a GUI
RUN apt-get update && apt-get install -y python3-pip \
    && pip3 install --no-cache-dir jinja2 numpy pyvista

# Create a directory for our wrapper scripts
WORKDIR /app

# Copy our Python wrapper and our Template Simulation Case
COPY ./wrapper_script.py /app/wrapper.py
COPY ./ray_manager.py /app/ray_manager.py
COPY ./base_case_templates /app/templates

# Set the entrypoint to our Python script, not the shell
ENTRYPOINT ["python3", "/app/wrapper.py"]
