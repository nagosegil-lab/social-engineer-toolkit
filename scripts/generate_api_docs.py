#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate API documentation (Markdown) for public Python APIs in this repository.
- Scans: /workspace/src and /workspace/modules
- Outputs: /workspace/docs/api/<mirrored-path>.md

It extracts module docstrings, public functions, classes, and methods using AST
without importing modules, so it is safe and side-effect free.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

REPO_ROOT = Path('/workspace')
SCAN_DIRS = [REPO_ROOT / 'src', REPO_ROOT / 'modules']
OUT_ROOT = REPO_ROOT / 'docs' / 'api'

# Some repos may not run from /workspace; allow override
if 'REPO_ROOT' in os.environ:
    REPO_ROOT = Path(os.environ['REPO_ROOT']).resolve()
    SCAN_DIRS = [REPO_ROOT / 'src', REPO_ROOT / 'modules']
    OUT_ROOT = REPO_ROOT / 'docs' / 'api'


def read_text_safely(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return None


def get_import_path(file_path: Path) -> Optional[str]:
    """Return dotted import path if under a Python package (currently under src/)."""
    try:
        rel = file_path.relative_to(REPO_ROOT)
    except ValueError:
        return None
    parts = list(rel.parts)
    if not parts:
        return None
    # Only advertise import path for code under src/
    if parts[0] != 'src':
        return None
    module_parts = parts[:]  # copy
    if module_parts[-1].endswith('.py'):
        module_parts[-1] = module_parts[-1][:-3]
    return '.'.join(module_parts)


def stringify_default(value_node: ast.AST) -> str:
    # Best-effort readable default representation
    try:
        # Python 3.9+: ast.unparse available; fall back otherwise
        unparse = getattr(ast, 'unparse', None)
        if unparse is not None:
            return unparse(value_node)
    except Exception:
        pass
    # Fallback simple types
    if isinstance(value_node, ast.Constant):
        return repr(value_node.value)
    if isinstance(value_node, (ast.List, ast.Tuple, ast.Set, ast.Dict)):
        return '...'
    return '...'


def build_signature(args: ast.arguments) -> Tuple[str, List[str]]:
    """
    Build a Python-like signature string and a list of arg names for example calls.
    Returns (signature_string, arg_names_for_example)
    """
    # Positional-only args (Python 3.8+)
    posonly = getattr(args, 'posonlyargs', []) or []
    normal = args.args or []
    kwonly = args.kwonlyargs or []

    all_pos = posonly + normal

    # Map defaults to the rightmost positional parameters
    defaults = args.defaults or []
    num_defaults = len(defaults)
    pos_names: List[str] = [a.arg for a in all_pos]
    sig_parts: List[str] = []

    for i, a in enumerate(all_pos):
        name = a.arg
        has_default = i >= (len(all_pos) - num_defaults)
        if has_default:
            default_node = defaults[i - (len(all_pos) - num_defaults)]
            default_str = stringify_default(default_node)
            sig_parts.append(f"{name}={default_str}")
        else:
            sig_parts.append(name)

    # *args
    if args.vararg is not None:
        sig_parts.append(f"*{args.vararg.arg}")

    # kw-only args
    for i, a in enumerate(kwonly):
        default_node = None
        if args.kw_defaults and args.kw_defaults[i] is not None:
            default_node = args.kw_defaults[i]
        if default_node is not None:
            default_str = stringify_default(default_node)
            sig_parts.append(f"{a.arg}={default_str}")
        else:
            sig_parts.append(a.arg)

    # **kwargs
    if args.kwarg is not None:
        sig_parts.append(f"**{args.kwarg.arg}")

    signature = f"({', '.join(sig_parts)})"

    # Prepare example call args: use only required positional + kwargs with defaults omitted
    example_args: List[str] = []

    # Required positional (without defaults)
    for i, a in enumerate(all_pos):
        name = a.arg
        has_default = i >= (len(all_pos) - num_defaults)
        if not has_default:
            example_args.append(f"{name}=...")

    # Provide at most one kw-only example
    if kwonly:
        example_args.append(f"{kwonly[0].arg}=...")

    return signature, example_args


def sanitize_docstring(doc: Optional[str]) -> str:
    if not doc:
        return "No docstring provided."
    # Normalize newlines and strip leading/trailing whitespace
    return doc.strip()


def markdown_escape(text: str) -> str:
    return text.replace('<', '&lt;').replace('>', '&gt;')


def generate_module_markdown(file_path: Path, tree: ast.AST, source: str) -> str:
    rel = file_path.relative_to(REPO_ROOT)
    import_path = get_import_path(file_path)

    module_doc = sanitize_docstring(ast.get_docstring(tree, clean=True))

    public_functions: List[ast.FunctionDef] = []
    public_classes: List[ast.ClassDef] = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith('_'):
                public_functions.append(node)
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith('_'):
                public_classes.append(node)

    lines: List[str] = []
    lines.append(f"# Module: `{rel.as_posix()}`")
    if import_path:
        lines.append("")
        lines.append(f"Import path: `{import_path}`")
    lines.append("")
    lines.append("## Module docstring")
    lines.append("")
    lines.append(module_doc)

    if import_path:
        lines.append("")
        lines.append("## Basic import example")
        lines.append("")
        lines.append("```python")
        lines.append(f"from {import_path} import <symbol>")
        lines.append("# <symbol> can be a function or class from this module")
        lines.append("```")
    else:
        # For non-packaged modules, show import-by-path pattern once per module
        lines.append("")
        lines.append("## Importing by file path")
        lines.append("")
        lines.append("```python")
        lines.append("import importlib.util")
        lines.append(f"spec = importlib.util.spec_from_file_location(\"{file_path.stem}\", \"{file_path.as_posix()}\")")
        lines.append("mod = importlib.util.module_from_spec(spec)")
        lines.append("spec.loader.exec_module(mod)")
        lines.append("# Now use: mod.<symbol>(...) or mod.<Class>(...)")
        lines.append("```")

    if public_functions:
        lines.append("")
        lines.append("## Functions")
        for fn in public_functions:
            signature, example_args = build_signature(fn.args)
            lines.append("")
            lines.append(f"### `{fn.name}{signature}`")
            fn_doc = sanitize_docstring(ast.get_docstring(fn, clean=True))
            lines.append("")
            lines.append(fn_doc)
            # Example
            example_module_ref = (f"from {import_path} import {fn.name}" if import_path else "# see import-by-path snippet above\n{alias} = mod")
            lines.append("")
            lines.append("```python")
            if import_path:
                lines.append(example_module_ref)
                call_args = ", ".join(example_args)
                lines.append(f"result = {fn.name}({call_args})")
            else:
                call_args = ", ".join(example_args)
                lines.append("# After running the import-by-path snippet above:")
                lines.append(f"result = mod.{fn.name}({call_args})")
            lines.append("```")

    if public_classes:
        lines.append("")
        lines.append("## Classes")
        for cls in public_classes:
            cls_doc = sanitize_docstring(ast.get_docstring(cls, clean=True))
            lines.append("")
            lines.append(f"### `{cls.name}`")
            lines.append("")
            lines.append(cls_doc)

            # Constructor signature if available
            init_fn = None
            for node in cls.body:
                if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                    init_fn = node
                    break
            if init_fn is not None:
                signature, example_args = build_signature(init_fn.args)
            else:
                signature, example_args = '(...)', []

            # Class example
            lines.append("")
            lines.append("```python")
            if import_path:
                lines.append(f"from {import_path} import {cls.name}")
                ctor_args = ", ".join(example_args)
                lines.append(f"obj = {cls.name}({ctor_args})")
            else:
                lines.append("# After running the import-by-path snippet above:")
                ctor_args = ", ".join(example_args)
                lines.append(f"obj = mod.{cls.name}({ctor_args})")
            lines.append("# Call a method (if available):")
            # Show first public method other than __init__ if present
            method_shown = False
            for node in cls.body:
                if isinstance(node, ast.FunctionDef) and not node.name.startswith('_') and node.name != '__init__':
                    m_sig, m_args = build_signature(node.args)
                    # Strip first arg (self)
                    call_args = ", ".join(a for a in m_args if not a.startswith('self='))
                    lines.append(f"obj.{node.name}({call_args})")
                    method_shown = True
                    break
            if not method_shown:
                lines.append("# (no public methods detected)")
            lines.append("```")

            # Methods documentation
            method_items = [n for n in cls.body if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')]
            if method_items:
                lines.append("")
                lines.append(f"#### Methods")
                for m in method_items:
                    m_sig, _ = build_signature(m.args)
                    lines.append("")
                    lines.append(f"- `{m.name}{m_sig}`")
                    m_doc = sanitize_docstring(ast.get_docstring(m, clean=True))
                    if m_doc:
                        lines.append(f"  - {m_doc}")

    return '\n'.join(lines) + '\n'


def process_file(py_file: Path) -> Optional[Tuple[Path, str]]:
    source = read_text_safely(py_file)
    if source is None:
        return None
    try:
        tree = ast.parse(source)
    except Exception:
        return None

    rel = py_file.relative_to(REPO_ROOT)
    out_rel = rel.with_suffix('.md')
    out_path = OUT_ROOT / out_rel
    # Ensure parent directories
    out_path.parent.mkdir(parents=True, exist_ok=True)

    md = generate_module_markdown(py_file, tree, source)
    return out_path, md


def should_include(path: Path) -> bool:
    if path.suffix != '.py':
        return False
    name = path.name
    # Skip obvious non-library scripts in root level of repo
    if path.parent == REPO_ROOT and name in {'setoolkit', 'seautomate', 'seproxy', 'seupdate', 'setup.py'}:
        return False
    return True


def main() -> int:
    files: List[Path] = []
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for root, _dirs, filenames in os.walk(base):
            for fn in filenames:
                p = Path(root) / fn
                if should_include(p):
                    files.append(p)

    generated: List[Path] = []
    for f in files:
        result = process_file(f)
        if result is None:
            continue
        out_path, md = result
        try:
            out_path.write_text(md, encoding='utf-8')
            generated.append(out_path)
        except Exception as e:
            print(f"[!] Failed to write {out_path}: {e}")

    # Also emit a simple index file automatically
    index_path = OUT_ROOT / 'INDEX.md'
    try:
        lines = ["# API Index", ""]
        for p in sorted(generated):
            rel = p.relative_to(OUT_ROOT)
            display = rel.as_posix()
            lines.append(f"- [{display}]({display})")
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    except Exception as e:
        print(f"[!] Failed to write index: {e}")

    print(f"Generated {len(generated)} documentation files under {OUT_ROOT}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
