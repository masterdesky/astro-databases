# astro-databases

Teaching notebooks for querying the SDSS database (CasJobs and SkyServer) from Python with SciServer's [SciScript-Python](https://github.com/sciserver/SciScript-Python) library. The notebooks in `notebooks/` run unchanged on SciServer Compute and on a local machine.

## Local setup

Install [uv](https://docs.astral.sh/uv/), then in the repository root run:

```sh
uv sync
uv run jupyter lab
```

`uv sync` creates `.venv/` with all dependencies, including SciScript-Python pinned to a fixed commit of its GitHub repository (it is not on PyPI).

Figure text is typeset by LaTeX when `latex` and `dvipng` are installed, together with the cm-super fonts (on Debian and Ubuntu: `texlive-latex-extra`, `cm-super` and `dvipng`). Without them, matplotlib draws the text with its own STIX fonts.

The demo notebooks need no [SciServer](https://www.sciserver.org/) account, as they run only synchronous CasJobs queries and SkyServer image cutouts, which work without login. Neither does the intro notebook, `intro-casjobs-and-functions.ipynb`, except its last section, on batch jobs and MyDB. That section needs a SciServer account. If you run it inside SciServer Compute, the notebook is logged in already; on a local machine it asks for the username and password.

## Settings

`notebooks/settings.py` holds the data releases, the center of the Coma cluster, cosmology, cutout framing, the fiber aperture correction of velocity dispersions and plot styles. `notebooks/parameter_sets.json` holds the parameters of each notebook section (search radii, sample limits, gallery grids, map strips), and `notebooks/tracers.json` the samples (tracers) drawn in the multi-tracer map. Setting the environment variable `SDSS_NOTEBOOKS_PARAMETER_SET=light` switches the intro and demo notebooks to small queries for quick checks.
