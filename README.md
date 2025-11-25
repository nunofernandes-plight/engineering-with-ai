# engineering-with-ai
Engineering workloads with new Artificial Intelligence built-in. SaaS platform for Engineers

## Setup & Installation

To install Python dependencies (Ray, NumPy), run:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Quick verification (runs a short Python snippet to import Ray):

```bash
python3 scripts/check_ray.py
```

Notes:
- The workspace expects a local Python 3.12+ runtime (the devcontainer includes this by default).
- Ray is a distributed library — running cluster workloads requires a Ray cluster or Kubernetes configuration. Use `ray_manager.py` to start/connect a cluster and dispatch jobs.

## Docker (OpenFOAM) Image

This repo includes a `Dockerfile` which builds an image based on `opencfd/openfoam-default:2306`.

Build image:

```bash
docker build -t engineering-with-ai:openfoam .
```

Run container:

```bash
docker run --rm -v $(pwd)/base_case_templates:/app/templates engineering-with-ai:openfoam

Run the included wrapper inside the container (it will render templates into /tmp/sim_case):

```bash
docker run --rm -v $(pwd)/base_case_templates:/app/templates engineering-with-ai:openfoam python3 /app/wrapper.py
```

You can also run the manager (if desired) from inside the image:

```bash
docker run --rm -v $(pwd)/base_case_templates:/app/templates engineering-with-ai:openfoam python3 /app/ray_manager.py
```

Template files
---------------
The repository ships an example template at `base_case_templates/0/U.jinja` using a simple Jinja2 variable `{{ inlet_velocity_x }}`. You can add more templates here and use the wrapper to render them as part of case setup.
```

Notes:
- The image installs Python 3 and a few Python packages used for templating and post-processing. You can add more in the `Dockerfile`.
- `wrapper_script.py` is used as the container entrypoint — replace with your active wrapper implementation that performs case generation, runs the solver, and extracts results.
