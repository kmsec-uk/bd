import ast
import builtins
import argparse

"""
BD - Builtins Defang, an experimental way to perform quick analysis on Python malware samples
"""

class BDError(Exception):
    pass


unsafe_exec = builtins.exec

def catch_exec(code, globals=None, locals=None) -> str:
    """Catch calls to builtins.exec. and if deemed `imsafe`"""
    # if "__name__" is not defined, this is user-defined code which is unsafe.
    if not globals:
        print(f"🤖 Intercepted exec:\r\n\r\n```\r\n{code}\r\n```\r\n")
        return
    # manually allowlisted exec contexts:
    elif globals["__name__"] in [
        "getopt",
        "traceback",
        "struct",
        "gettext",
        "warnings",
        "_colorize",
        "textwrap",
        "collections.abc",
        "linecache",
        "tokenize",
        "token",
        "locale",
        "lzma",
        "_compression",
        "bz2",
        "fnmatch",
        "shutil"
    ]:
        return unsafe_exec(code, globals=globals, locals=locals)
    elif globals["__name__"] in [
        "base64"
    ]:
        print(f"🤖 ❗ Executing in the context of {globals['__name__']}")
        return unsafe_exec(code, globals=globals, locals=locals)
    else:
        raise BDError(f"🤖 I don't want to exec in {globals['__name__']}")

# Patch the built-in exec
builtins.exec = catch_exec


def review_imports(imports: list[ast.Import]) -> None:
    if len(imports) > 0:
        if len(imports[0].names) > 1:
            raise BDError("I found too many imports :(. Wowee")
        alias = imports[0].names[0]
        print(
            f"🤖 This sample imports {alias.name} as {alias.asname if alias.asname else alias.name}"
        )
        if alias.name != "base64":
            raise BDError("🤖 I can't handle anything except base64 imports, it's scary.")


def triage_ast(sample):
    expressions = []
    imports = []
    sample_ast = ast.parse(sample, mode="exec")
    for node in ast.walk(sample_ast):
        if isinstance(node, ast.Expr):  # Check for ast.Expr
            expressions.append(node)
        if isinstance(node, ast.Import):  # Check for ast.Import
            imports.append(node)
    if len(imports) > 1:
        raise BDError(
            "🤖 I don't want to analyse this anymore.\n"
            + f"I found {len(imports)} imports amd {len(expressions)} expressions. I can't handle this!"
        )
    review_imports(imports)

    expr = expressions[0].value
    for expr in [x.value for x in expressions]:
        if not isinstance(expr, ast.Call):
            raise BDError(f"I can't handle {type(expr)}")
        if expr.func.id not in ["print", "exec"]:
            raise BDError(
                f"🤖 I can't handle anything except exec and print for now. Found {expr.func.id}"
            )


def process_file(file_path):
    with open(file_path, 'rt') as file:
        content = file.read()
        print(f"🤖 Processing {file_path}")
        triage_ast(content)
        unsafe_exec(content)
        print(f"🤖 Done with {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a file.",
        usage="python bd.py [-h] <file>",
    )
    parser.add_argument(
        "file", type=str, help="Path to the input file"
    )
    args = parser.parse_args()
    process_file(args.file)