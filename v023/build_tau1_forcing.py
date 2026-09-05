#!/usr/bin/env python3
import importlib.util
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
path = repo/'v022'/'build_offline_forcing.py'
spec = importlib.util.spec_from_file_location('v022_build_offline_forcing', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.TAUS = [('t1',1.0)]
mod.main()
