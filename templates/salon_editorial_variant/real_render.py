import argparse
import json
import sys
from pathlib import Path
import render as R
ROOT=Path(__file__).resolve().parent

def merge_profile(base, override):
    merged=dict(base)
    for key,value in override.items():
        if key=="extends":
            continue
        if isinstance(value,dict) and isinstance(merged.get(key),dict):
            merged[key]=merge_profile(merged[key],value)
        else:
            merged[key]=value
    return merged

def load_profile(path, seen=None):
    seen=seen or set()
    if path in seen:
        raise RuntimeError(f"profile extends cycle: {path.name}")
    seen.add(path)
    data=json.loads(path.read_text(encoding="utf-8"))
    parent=data.get("extends")
    if parent:
        base_path=path.parent/parent
        data=merge_profile(load_profile(base_path,seen),data)
    return data


def profile_paths(names):
    if not names:
        return sorted((ROOT/"real_profiles").glob("*.json"))
    paths=[]
    for name in names:
        path=Path(name)
        if not path.is_absolute():
            path=ROOT/"real_profiles"/name
        paths.append(path)
    return paths


def render_profiles(paths, out):
    out.mkdir(parents=True,exist_ok=True)
    bad=0
    for pf in paths:
        p=load_profile(pf)
        page=R.render(p); hits=R.scan_forbidden(page)
        d=out/p.get("output_slug",pf.stem); d.mkdir(parents=True,exist_ok=True)
        (d/"index.html").write_text(page,encoding="utf-8")
        for key in ("hero_image","band_image","story_image"):
            v=p.get(key)
            if v and not str(v).startswith(("http","data:","/")):
                src=ROOT/v
                if src.exists(): (d/Path(v).name).write_bytes(src.read_bytes())
        print(f"[{'PASS' if not hits else 'FORBIDDEN '+str(hits)}] {pf.stem} ({len(page)}b)")
        bad += 1 if hits else 0
    return 1 if bad else 0


def main(argv=None):
    parser=argparse.ArgumentParser(description="Render real salon editorial profiles.")
    parser.add_argument("--profile", action="append", default=[], help="Profile filename or path. Repeatable.")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT.parent.parent/"generated_demos"/"real_lead_review_20260617"),
        help="Directory that receives one folder per rendered profile.",
    )
    args=parser.parse_args(argv)
    return render_profiles(profile_paths(args.profile), Path(args.output_dir))


if __name__ == "__main__":
    sys.exit(main())
