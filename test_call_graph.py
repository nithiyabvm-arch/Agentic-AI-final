from pprint import pprint

from context_builder.discovery.include_discovery import (
    discover_include_paths
)

from context_builder.discovery.compiler_flag_discovery import (
    discover_compiler_flags
)

from context_builder.call_graph_clang import (
    build_call_graph_clang
)

project_root = r"C:\Users\acer\Downloads\Nithiya_poc\HVAC"

include_paths = discover_include_paths(
    project_root
)

flags = discover_compiler_flags(
    f"{project_root}/Debug"
)

call_graph = build_call_graph_clang(
    project_root,
    include_paths,
    flags["defines"]
)

pprint(call_graph)
