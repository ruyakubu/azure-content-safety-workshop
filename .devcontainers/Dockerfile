FROM mcr.microsoft.com/devcontainers/miniconda:0-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
RUN conda install -n base -c conda-forge mamba
COPY /lib/env.yaml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/lib/env.yaml" ]; then umask 0002 && /opt/conda/bin/mamba env create -f /tmp/conda-tmp/lib/env.yaml; fi \
    && rm -rf /tmp/conda-tmp


