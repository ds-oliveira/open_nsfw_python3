# open_nsfw_python3

A Python 3 library that wraps Yahoo's open_nsfw convolutional neural network (ResNet-50, Caffe) to score images for sexual content, returning a probability from 0.0 (safe) to 1.0 (explicit).

## Tech Stack

- **Language:** Python 3.6+
- **Framework:** None (pure Python installable library)
- **Package manager:** pip / `setup.py`
- **Core dependencies:** `numpy>=1.16.4`, `image>=1.5.27` (Pillow wrapper), `caffe` (system package — not on PyPI)
- **ML model:** Yahoo's ResNet-50 NSFW Caffe model (`resnet_50_1by2_nsfw.caffemodel` + `deploy.prototxt`), bundled inside the package
- **Containerisation:** Docker (`python:3.7.4` base + `caffe-cpu` via apt)
- **Testing:** None configured
- **Linting/Formatting:** None configured

## Project Structure

- `open_nsfw_python3/` — The installable package directory
- `open_nsfw_python3/__init__.py` — Full implementation: `NSFWClassifier` class with `resize_image`, `caffe_preprocess_and_compute`, and `get_score` methods
- `open_nsfw_python3/deploy.prototxt` — Caffe network architecture definition (60 KB); **do not edit**
- `open_nsfw_python3/resnet_50_1by2_nsfw.caffemodel` — Pre-trained model weights (~23 MB); **do not edit**
- `open_nsfw_python3/README.md` — Copy of root README, bundled into the PyPI distribution via `package_data`
- `open_nsfw_python3/LICENSE.md` — BSD 2-Clause licence (Yahoo Inc.), also bundled
- `setup.py` — Package metadata, version, dependency declarations, and `package_data` (bundles `.caffemodel`, `.prototxt`, `.md`)
- `Dockerfile` — Reference environment: installs `caffe-cpu` via apt and sets `PYTHONPATH`
- `README.md` — Usage documentation and installation guide

## Common Commands

```bash
# Install from PyPI
pip install open-nsfw-python3

# Install in editable/development mode (after cloning)
pip install -e .

# Build distribution archives
python setup.py sdist bdist_wheel

# Upload to PyPI (requires twine)
twine upload dist/*

# Build the Docker reference environment
docker build -t open_nsfw_python3:latest .

# Quick usage check (inside a properly configured environment)
python -c "
from open_nsfw_python3 import NSFWClassifier
classifier = NSFWClassifier()
print(classifier.get_score('image.jpg'))
"
```

> ⚠️ **`caffe` is not installable via pip.** It must be installed from the system package manager. See the Docker environment section below.

## Key Conventions

- **Single-class API** — the entire public interface is `NSFWClassifier`, exported from `open_nsfw_python3/__init__.py`. Do not add module-level functions; keep the class-based interface.
- **`get_score(filepath)`** is the only public method — it accepts a local file path string and returns a `float`. Keep this contract stable.
- **Internal helpers are instance methods** — `resize_image` and `caffe_preprocess_and_compute` are not part of the public API; prefix them with `_` if you refactor.
- **Model files are loaded from `pkg_resources.resource_filename`** — this is how the bundled `.caffemodel` and `.prototxt` are located after pip install. Do not hardcode absolute paths.
- **Image preprocessing is hardcoded** — mean subtraction values `[104, 117, 123]` and channel swap `(2, 1, 0)` match the training configuration of the Yahoo model. Do not change these without retraining.
- **`snake_case`** everywhere — file names, method names, variable names, and the package name.
- **Version is hardcoded in `setup.py`** — bump manually before each PyPI release.
- **Docstrings** use a plain-text NumPy-style layout. Keep new docstrings consistent.

## Environment Setup

`caffe` **cannot be installed via pip**. Use Docker (recommended) or install manually on Linux:

### Docker (recommended)

```bash
docker build -t open_nsfw_python3:latest .
docker run -it open_nsfw_python3:latest python
```

The Dockerfile:
1. Starts from `python:3.7.4`
2. Runs `apt update && apt install caffe-cpu --yes`
3. Sets `ENV PYTHONPATH=/usr/lib/python3/dist-packages:` so Python can find the apt-installed `caffe` module

### Manual (Linux only)

```bash
sudo apt update && sudo apt install caffe-cpu -y
export PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH
pip install numpy>=1.16.4 "image>=1.5.27"
pip install open-nsfw-python3
```

### Required environment variables

| Variable | Value | Purpose |
|---|---|---|
| `PYTHONPATH` | `/usr/lib/python3/dist-packages:` | Exposes the apt-installed `caffe` package to Python |

## Notes for AI Agents

- **`caffe` is the critical system dependency** — `import caffe` will fail unless `caffe-cpu` (or `caffe-gpu`) is installed via `apt` and `PYTHONPATH` is set correctly. Every code path that classifies an image requires caffe.
- **`deploy.prototxt` and `resnet_50_1by2_nsfw.caffemodel` must never be edited** — they are the pre-trained Yahoo model artefacts. They are bundled via `package_data` in `setup.py` and loaded at runtime via `pkg_resources`.
- **The model is reloaded on every `get_score()` call** — `caffe.Net(...)` is instantiated inside `get_score`, not in `__init__`. This is intentional for simplicity but is slow. If you refactor to cache the model, test carefully for thread-safety.
- **`resize_image` mutates the file on disk** — it opens the image, resizes it, and saves it back to the same path before wrapping it in a `BytesIO`. Be aware of this if you call the method directly.
- **No tests exist** — there is no `tests/` directory, no `pytest`, and no CI. If you add functionality, create a `tests/` directory with `pytest`.
- **`dist/`, `build/`, `*.egg-info/`** are generated by `setup.py`; never commit them. `__pycache__` is also gitignored.
- **`README.md` and `LICENSE.md` are duplicated** — copies exist at the repo root and inside `open_nsfw_python3/` for PyPI bundling. Update **both** if you change documentation.
- **Python 3.6+ only** — `python_requires='>=3.6'`. Do not use features introduced after Python 3.6 without bumping this constraint.
- **`image` package** (`pip install image`) is a thin Pillow wrapper; `PIL.Image` is what is actually used. Do not confuse `image` (PyPI) with `Pillow` (PyPI) when adding dependencies.
