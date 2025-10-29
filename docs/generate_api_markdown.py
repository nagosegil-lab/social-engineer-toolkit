#!/usr/bin/env python3
import ast
import os
import textwrap
from typing import List, Optional, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ROOT = os.path.join(REPO_ROOT, "src")
OUT_ROOT = os.path.join(REPO_ROOT, "docs", "api_md")

# Utilities

def get_module_name(py_path: str) -> str:
    rel = os.path.relpath(py_path, REPO_ROOT)
    # Normalize path separators and strip .py
    parts = rel.replace(os.sep, "/").split("/")
    if parts[0] != "src":
        raise ValueError(f"Expected file under src/: {py_path}")
    mod_parts = parts  # includes 'src'
    mod_parts[-1] = mod_parts[-1][:-3]  # strip .py
    return ".".join(mod_parts)


def render_signature(func: ast.AST) -> str:
    if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return "()"

    args: ast.arguments = func.args

    def fmt_arg(a: ast.arg, default: Optional[str] = None) -> str:
        name = a.arg
        if default is not None:
            return f"{name}={default}"
        return name

    posonly = getattr(args, "posonlyargs", [])
    regular = args.args
    defaults = list(args.defaults)
    # Align defaults to the rightmost positional args
    pad = len(regular) - len(defaults)
    default_strs: List[Optional[str]] = [None] * max(pad, 0) + ["…"] * len(defaults)

    parts: List[str] = []

    # Pos-only args (Python 3.8+)
    if posonly:
        parts.extend(fmt_arg(a) for a in posonly)
        parts.append("/")

    # Regular positional args
    for a, d in zip(regular, default_strs):
        parts.append(fmt_arg(a, d))

    # *args
    if args.vararg is not None:
        parts.append("*" + args.vararg.arg)
    elif getattr(args, "kwonlyargs", []):
        # Explicit * to mark start of kw-only if no *args
        parts.append("*")

    # Keyword-only args (Python 3 only; be defensive for legacy syntax)
    kwonlyargs = getattr(args, "kwonlyargs", [])
    kwonlydefaults = getattr(args, "kwonlydefaults", [])
    # Align defaults to the rightmost kw-only args
    pad_k = len(kwonlyargs) - len(kwonlydefaults)
    kwdefaults_aligned: List[Optional[str]] = [None] * max(pad_k, 0) + ["…"] * len(kwonlydefaults)
    for a, d in zip(kwonlyargs, kwdefaults_aligned):
        # kwonlydefaults entries may be None; render as required when None
        dval = "…" if d is not None else None
        parts.append(fmt_arg(a, dval))

    # **kwargs
    if args.kwarg is not None:
        parts.append("**" + args.kwarg.arg)

    return f"({', '.join(parts)})"


def collect_module_api(py_path: str) -> Tuple[str, str, List[Tuple[str, str, str]], List[Tuple[str, str, List[Tuple[str, str, str]]]]]:
    with open(py_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename=py_path)
    module_doc = ast.get_docstring(tree) or ""

    functions: List[Tuple[str, str, str]] = []  # (name, signature, doc)
    classes: List[Tuple[str, str, List[Tuple[str, str, str]]]] = []  # (name, doc, methods)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue
            doc = ast.get_docstring(node) or ""
            sig = render_signature(node)
            functions.append((node.name, sig, doc))
        elif isinstance(node, ast.ClassDef):
            if node.name.startswith("_"):
                continue
            cdoc = ast.get_docstring(node) or ""
            methods: List[Tuple[str, str, str]] = []
            for n in node.body:
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if n.name.startswith("_"):
                        continue
                    mdoc = ast.get_docstring(n) or ""
                    msig = render_signature(n)
                    methods.append((n.name, msig, mdoc))
            classes.append((node.name, cdoc, methods))

    module_name = get_module_name(py_path)
    return module_name, module_doc, functions, classes


def write_module_md(module_name: str, module_doc: str, functions, classes) -> None:
    # Map module name like src.core.setcore -> docs/api_md/src/core/setcore.md
    out_path = os.path.join(OUT_ROOT, *module_name.split(".")) + ".md"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    lines: List[str] = []
    lines.append(f"## {module_name}")
    lines.append("")
    if module_doc:
        lines.append(textwrap.dedent(module_doc).strip())
        lines.append("")

    if functions:
        lines.append("### Functions")
        lines.append("")
        for name, sig, doc in sorted(functions, key=lambda x: x[0].lower()):
            lines.append(f"- **{name}**")
            lines.append("")
            lines.append(f"  ```python\n{ 'def ' + name + sig }: ...\n  ```")
            if doc:
                lines.append("")
                lines.append(textwrap.indent(textwrap.dedent(doc).strip(), prefix="  "))
            lines.append("")

    if classes:
        lines.append("### Classes")
        lines.append("")
        for cname, cdoc, methods in sorted(classes, key=lambda x: x[0].lower()):
            lines.append(f"- **{cname}**")
            if cdoc:
                lines.append("")
                lines.append(textwrap.indent(textwrap.dedent(cdoc).strip(), prefix="  "))
            if methods:
                lines.append("")
                lines.append("  - Methods")
                lines.append("")
                for mname, msig, mdoc in sorted(methods, key=lambda x: x[0].lower()):
                    lines.append(f"    - `{mname}{msig}`")
                    if mdoc:
                        lines.append(textwrap.indent(textwrap.dedent(mdoc).strip(), prefix="      "))
                lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def write_index_md(modules: List[str]) -> None:
    out_path = os.path.join(OUT_ROOT, "index.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    lines = [
        "## API Reference (static, AST-based)",
        "",
        "- This index is generated without importing modules, avoiding side effects.",
        "- For richer docs where possible, also see the HTML API (if generated) at ../api/index.html.",
        "",
    ]
    for m in sorted(modules):
        rel = m.replace(".", "/") + ".md"
        lines.append(f"- [{m}]({rel})")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def should_skip(path: str) -> bool:
    # Skip clearly non-library or dangerous-on-import modules
    base = os.path.basename(path)
    if base.endswith(".py") is False:
        return True
    # Always include __init__.py to capture package docs
    return False


def main() -> None:
    modules_written: List[str] = []
    for root, _dirs, files in os.walk(SRC_ROOT):
        for fname in files:
            path = os.path.join(root, fname)
            if should_skip(path):
                continue
            try:
                module_name, module_doc, functions, classes = collect_module_api(path)
                write_module_md(module_name, module_doc, functions, classes)
                modules_written.append(module_name)
            except Exception as e:
                # Best-effort: skip files that cannot be parsed
                # Print to stderr for visibility if run manually
                print(f"[warn] Skipping {path}: {e}")
                continue
    write_index_md(modules_written)
    print(f"Wrote {len(modules_written)} module pages under {OUT_ROOT}")

if __name__ == "__main__":
    main()
