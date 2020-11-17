import ast
import imp
import os
import sys
from collections import namedtuple
from typing import List

Import = namedtuple("Import", ["module", "name", "alias"])


def get_imports(path: str) -> List[Import]:
    with open(path) as fh:
        root = ast.parse(fh.read(), path)

    imports: List[Import] = []

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split(".")
        else:
            continue

        for n in node.names:
            imports.append(Import(module, n.name.split("."), n.asname))

    return imports


def is_stdlib(mod_name: str) -> bool:
    python_path = os.path.dirname(sys.executable)

    if imp.is_builtin(mod_name):
        return True

    try:
        module_path = imp.find_module(mod_name)[1]

        print(python_path)
        print(module_path)

        if "site-packages" in module_path:
            return True

        if python_path in module_path:
            return True

        return False
    except ImportError:
        return False


print(sys.argv)


for imported in get_imports(sys.argv[1]):
    # print(imported)

    if len(imported.module) == 0:
        import_name = ".".join(imported.name)
    else:
        import_name = ".".join(imported.module)

    # print(import_name)

    if is_stdlib(import_name):
        print(imported)
