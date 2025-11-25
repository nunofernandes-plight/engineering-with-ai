#!/usr/bin/env python3
import os
import jinja2
from pathlib import Path

# Minimal wrapper script placeholder for building the Docker image.
# This demonstrates rendering Jinja2 templates from `base_case_templates`.

TEMPLATE_DIR = Path('/app/templates') if Path('/app/templates').exists() else Path('./base_case_templates')
OUTPUT_DIR = Path('/tmp/sim_case')

def render_template(filename: str, context: dict, out_dir: Path) -> Path:
    loader = jinja2.FileSystemLoader(str(TEMPLATE_DIR))
    env = jinja2.Environment(loader=loader)
    template = env.get_template(filename)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / filename.replace('.jinja', '')
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('w') as fh:
        fh.write(template.render(**context))
    return target

def main():
    print("Wrapper script: rendering templated case into /tmp/sim_case...")
    context = {'inlet_velocity_x': 42.0}
    try:
        out = render_template('0/U.jinja', context, OUTPUT_DIR)
        print(f"Rendered {out}")
    except Exception as e:
        print("Template render failed:", e)

if __name__ == '__main__':
    main()
