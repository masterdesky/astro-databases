"""Shared settings for the SDSS database notebooks."""

import json
import os
import shutil
import subprocess
from pathlib import Path

from astropy.cosmology import Planck18
from cycler import cycler

# CasJobs serves DR17 and DR18 without login. DR17 is the final release
# of the SDSS-I to SDSS-IV galaxy and quasar surveys.
CASJOBS_CONTEXT = "DR17"
SKYSERVER_RELEASE = "DR20"

# Center of the Coma cluster (Abell 1656) in degrees, the sky region the
# intro notebook returns to in every section.
COMA_RA = 194.953
COMA_DEC = 27.981

COSMOLOGY = Planck18

# Pixel size of the SDSS camera in arcseconds. Cutouts with finer pixels
# only interpolate between the measured ones.
SDSS_PIXEL_SCALE = 0.396
# Field of view of a galaxy cutout, in units of the radius containing
# 90 % of the galaxy's Petrosian flux (petroR90_r).
CUTOUT_FIELD_OF_VIEW = 4
# Radius of an SDSS-I/II spectrograph fiber in arcseconds.
SDSS_FIBER_RADIUS = 1.5
# Velocity dispersion measured within radius r falls as r**-0.04
# (Jorgensen, Franx & Kjaergaard 1995). SDSS fiber dispersions are
# corrected to the value within a fixed fraction of each galaxy's
# effective radius, one eighth as in that paper.
APERTURE_CORRECTION_EXPONENT = 0.04
APERTURE_CORRECTION_FRACTION = 1 / 8

# "full" for lecture runs, "light" for quick checks.
PARAMETER_SET = os.environ.get("SDSS_NOTEBOOKS_PARAMETER_SET", "full")

PARAMETER_SETS_FILE = Path(__file__).with_name("parameter_sets.json")
TRACERS_FILE = Path(__file__).with_name("tracers.json")

# Okabe-Ito color-blind safe palette.
OKABE_ITO = [
    "#000000",
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
]

# Width of a full-width figure in inches, the text width of a two-column
# journal page. Printed at its own width, every figure keeps its font
# sizes.
FIGURE_WIDTH = 7

# Fonts, sizes and line widths shared by the light and dark styles.
BASE_STYLE = {
    "font.family": "serif",
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "legend.title_fontsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "legend.frameon": False,
    "figure.dpi": 200,
    "figure.constrained_layout.use": True,
    "lines.linewidth": 2,
    "lines.markersize": 5,
    "lines.markeredgewidth": 1,
    "axes.linewidth": 1,
    "axes.grid": False,
    "grid.linewidth": 0.8,
    "grid.linestyle": ":",
    "grid.alpha": 0.6,
    "xtick.bottom": True,
    "xtick.top": True,
    "ytick.left": True,
    "ytick.right": True,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.major.width": 1,
    "ytick.major.width": 1,
    "xtick.minor.width": 0.8,
    "ytick.minor.width": 0.8,
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "xtick.minor.size": 3,
    "ytick.minor.size": 3,
}

# LaTeX packages that matplotlib loads to typeset figure text, besides
# those of the LaTeX kernel.
TEX_PACKAGES = [
    "type1cm.sty",
    "type1ec.sty",
    "geometry.sty",
    "underscore.sty",
]


def tex_installed():
    """Availability of latex, dvipng and the TEX_PACKAGES."""
    tools = ["latex", "dvipng", "kpsewhich"]
    if not all(shutil.which(tool) for tool in tools):
        return False
    # kpsewhich exits with an error when a package is missing.
    found = subprocess.run(
        ["kpsewhich", *TEX_PACKAGES],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.split()
    return len(found) == len(TEX_PACKAGES)


# Figure text is typeset by LaTeX when it is installed, otherwise by
# matplotlib with the STIX fonts, which also cover the degree sign and
# the en dash.
if tex_installed():
    BASE_STYLE |= {
        "text.usetex": True,
        "font.serif": ["Computer Modern Roman"],
    }
else:
    BASE_STYLE |= {"font.serif": ["STIXGeneral"], "mathtext.fontset": "stix"}

# Background color #f4f0e8 after S. Conradi (@S_Conradi).
LIGHT_STYLE = BASE_STYLE | {
    "axes.prop_cycle": cycler(color=OKABE_ITO),
    "figure.facecolor": "#ffffff",
    "axes.facecolor": "#ffffff",
    "text.color": "0.15",
    "axes.labelcolor": "0.15",
    "axes.edgecolor": "0.15",
    "xtick.color": "0.15",
    "ytick.color": "0.15",
    "grid.color": "0.7",
}

# White takes the place of the palette's black.
DARK_STYLE = BASE_STYLE | {
    "axes.prop_cycle": cycler(color=["#FFFFFF", *OKABE_ITO[1:]]),
    "figure.facecolor": "black",
    "axes.facecolor": "black",
    "text.color": "0.85",
    "axes.labelcolor": "0.85",
    "axes.edgecolor": "0.85",
    "xtick.color": "0.85",
    "ytick.color": "0.85",
    "grid.color": "0.5",
}


def parameter_set(name):
    """Named parameters of a notebook section in the active set."""
    with open(PARAMETER_SETS_FILE) as f:
        return json.load(f)[name][PARAMETER_SET]


def tracers():
    """Tracer definitions of the multi-tracer wedge."""
    with open(TRACERS_FILE) as f:
        return json.load(f)
