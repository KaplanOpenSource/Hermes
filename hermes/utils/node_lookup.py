import ast
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from jinja2 import Environment, meta, nodes


class NodeParameter:
    def __init__(self, name: str, is_required: bool, source: str):
        self.name = name
        self.is_required = is_required
        self.source = source

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "is_required": self.is_required,
            "source": self.source
        }

class NodeOutput:
    def __init__(self, name: str, source: str):
        self.name = name
        self.source = source

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "source": self.source
        }

class NodeInfo:
    def __init__(self, node_type: str, parameters: List[NodeParameter], outputs: List[NodeOutput]):
        self.node_type = node_type
        self.parameters = parameters
        self.outputs = outputs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type,
            "parameters": [p.to_dict() for p in self.parameters],
            "outputs": [p.to_dict() for p in self.outputs],
        }

def extract_params_from_json(file_path: str) -> List[NodeParameter]:
    """Extracts parameters from jsonForm.json Execution.input_parameters."""
    params = []
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            input_params = data.get("Execution", {}).get("input_parameters", {})
            for key in input_params:
                params.append(NodeParameter(key, True, "jsonForm"))
    except Exception:
        pass
    return params

def extract_params_from_python(file_path: str) -> Tuple[List[NodeParameter], List[NodeOutput]]:
    """Extracts parameters from _defaultParameters method in executer.py."""
    params = []
    outputs = []
    try:
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "_defaultParameters":
                    # Look for return statement
                    for stmt in node.body:
                        if isinstance(stmt, ast.Return):
                            # We expect a dict call or constant dict
                            val = stmt.value
                            if isinstance(val, ast.Dict):
                                # Search keys for 'inputs'
                                for i, key in enumerate(val.keys):
                                    if isinstance(key, ast.Constant) and key.value == "inputs":
                                        input_val = val.values[i]
                                        if isinstance(input_val, ast.List):
                                            for elt in input_val.elts:
                                                if isinstance(elt, ast.Constant):
                                                    params.append(NodeParameter(elt.value, True, "python"))
                            elif isinstance(val, ast.Call) and getattr(val.func, 'id', '') == 'dict':
                                # Handle dict(...) call
                                keywords = [kw for kw in val.keywords if kw.arg == "inputs"]
                                if keywords:
                                    input_val = keywords[0].value
                                    if isinstance(input_val, ast.List):
                                        for elt in input_val.elts:
                                            if isinstance(elt, ast.Constant):
                                                params.append(NodeParameter(elt.value, True, "python"))
                if isinstance(node, ast.FunctionDef) and node.name == "run":
                    # Look for return statement
                    for stmt in node.body:
                        if isinstance(stmt, ast.Return):
                            # We expect a dict call(`dict(...)`) or constant dict(`[...]`)
                            val = stmt.value
                            if isinstance(val, ast.Dict):
                                for i, key in enumerate(val.keys):
                                    if isinstance(key, ast.Constant) and isinstance(key.value, str):
                                        outputs.append(NodeOutput(key.value, "python"))
                            elif isinstance(val, ast.Call) and getattr(val.func, 'id', '') == 'dict':
                                # Handle dict(...) call
                                for kw in val.keywords:
                                    outputs.append(NodeOutput(kw.arg, "python"))
                    pass
    except Exception:
        pass
    return (params, outputs)


def extract_params_from_jinja(file_path: str) -> List[NodeParameter]:
    """Extracts parameters from Jinja template files using AST analysis.
    Determines optionality based on guards (is defined, default filter, or if blocks).
    """
    params = []
    try:
        with open(file_path, 'r') as f:
            source = f.read()

        env = Environment()
        ast = env.parse(source)
        external_vars = meta.find_undeclared_variables(ast)

        # Track all usages of each variable path and whether they are guarded
        usage_guards: Dict[str, Set[bool]] = {}

        def get_full_path(node):
            """Recursively resolve the full dot-notation path of a variable access."""
            if isinstance(node, nodes.Name):
                return node.name
            if isinstance(node, nodes.Getattr):
                prefix = get_full_path(node.node)
                return f"{prefix}.{node.attr}" if prefix else None
            if isinstance(node, nodes.Call):
                # For method calls like fields.items(), we only care about the root object.
                # We resolve the function being called to get its path and strip the method name.
                func_path = get_full_path(node.node)
                if func_path:
                    parts = func_path.split('.')
                    return ".".join(parts[:-1]) if len(parts) > 1 else parts[0]
                return None
            return None

        def get_all_root_vars(node):
            """Find all root variable names referenced in a node."""
            roots = set()
            if isinstance(node, nodes.Name):
                roots.add(node.name)
            elif isinstance(node, nodes.Getattr):
                roots.update(get_all_root_vars(node.node))
            elif isinstance(node, (nodes.Filter, nodes.Test)):
                roots.update(get_all_root_vars(node.node))
            elif isinstance(node, nodes.Call):
                roots.update(get_all_root_vars(node.node))
                for arg in node.args:
                    roots.update(get_all_root_vars(arg))
            elif isinstance(node, nodes.Compare):
                # Use the a-priori known attributes for Jinja2 Compare nodes
                try:
                    roots.update(get_all_root_vars(node.expr))
                    for op in node.ops:
                        if hasattr(op, 'expr'):
                            roots.update(get_all_root_vars(op.expr))
                except AttributeError:
                    pass
            elif hasattr(node, 'body') and isinstance(node.body, list):
                for child in node.body:
                    roots.update(get_all_root_vars(child))
            elif hasattr(node, 'body') and not isinstance(node.body, list):
                roots.update(get_all_root_vars(node.body))
            return roots

        def walk(node, active_guards: Set[str], current_usage_guard: Optional[str] = None, is_child_of_expr: bool = False):
            """Traverse the AST to find variable usages and their guards."""
            if isinstance(node, nodes.If):
                test_roots = get_all_root_vars(node.test)
                new_guards = active_guards | test_roots

                # Body is guarded by these variables
                if isinstance(node.body, list):
                    for child in node.body:
                        walk(child, new_guards, current_usage_guard, False)
                elif node.body is not None:
                    walk(node.body, new_guards, current_usage_guard, False)

                if node.else_:
                    if isinstance(node.else_, list):
                        for child in node.else_:
                            walk(child, active_guards, current_usage_guard, False)
                    elif node.else_ is not None:
                        walk(node.else_, active_guards, current_usage_guard, False)
                return

            if isinstance(node, nodes.For):
                path = get_full_path(node.iter)
                if path and not is_child_of_expr:
                    root = path.split('.')[0]
                    if root in external_vars:
                        is_guarded = (root in active_guards)
                        usage_guards.setdefault(path, set()).add(is_guarded)

                if isinstance(node.body, list):
                    for child in node.body:
                        walk(child, active_guards, current_usage_guard, False)
                elif node.body is not None:
                    walk(node.body, active_guards, current_usage_guard, False)
                return

            if isinstance(node, nodes.Filter):
                path = get_full_path(node.node)
                if path and not is_child_of_expr:
                    root = path.split('.')[0]
                    is_guarded = (node.name == 'default') or (root in active_guards)
                    usage_guards.setdefault(path, set()).add(is_guarded)
                guard_for_child = root if (path and node.name == 'default') else None
                walk(node.node, active_guards, current_usage_guard=guard_for_child, is_child_of_expr=True)
                return

            if isinstance(node, nodes.Test):
                path = get_full_path(node.node)
                if path and not is_child_of_expr:
                    root = path.split('.')[0]
                    is_guarded = (node.name == 'defined') or (root in active_guards)
                    usage_guards.setdefault(path, set()).add(is_guarded)
                guard_for_child = root if (path and node.name == 'defined') else None
                walk(node.node, active_guards, current_usage_guard=guard_for_child, is_child_of_expr=True)
                return

            if isinstance(node, nodes.Getattr):
                path = get_full_path(node)
                if path and not is_child_of_expr:
                    root = path.split('.')[0]
                    if root in external_vars:
                        is_guarded = (root in active_guards) or (current_usage_guard == root)
                        usage_guards.setdefault(path, set()).add(is_guarded)
                walk(node.node, active_guards, current_usage_guard=current_usage_guard, is_child_of_expr=True)
                return

            if isinstance(node, nodes.Name):
                if node.name in external_vars and not is_child_of_expr:
                    is_guarded = (node.name in active_guards) or (current_usage_guard == node.name)
                    usage_guards.setdefault(node.name, set()).add(is_guarded)
                return

            # Recursive walk for other container nodes
            if hasattr(node, 'body'):
                if isinstance(node.body, list):
                    for child in node.body:
                        walk(child, active_guards, current_usage_guard, False)
                elif node.body is not None:
                    walk(node.body, active_guards, current_usage_guard, False)

            if isinstance(node, nodes.Output):
                for child in node.nodes:
                    walk(child, active_guards, current_usage_guard, False)

        walk(ast, set())

        # Now convert usages to NodeParameters
        for path, guards in usage_guards.items():
            is_optional = all(guards)
            params.append(NodeParameter(path, not is_optional, "template"))

    except Exception as exc:
        print(f"[hermes.utils.node_lookup] Warning: could not parse template {file_path}: {exc}")

    return params

def _resources_root() -> str:
    """Return the absolute path to the hermes Resources directory.
    Mirrors the logic in JinjaTransform._resources_root().
    """
    here = Path(__file__).resolve()
    
    candidate = here.parent.parent / "Resources"
    return str(candidate)

def get_all_node_types(resources_root: str=_resources_root()) -> Dict[str, NodeInfo]:
    """Scans resources root for node types and their parameters."""
    nodes_info = {}

    # Walk through Resources directory
    for root, dirs, files in os.walk(resources_root):
        # Skip hidden directories or __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        # Determine the relative path to use as node type
        rel_path = os.path.relpath(root, resources_root)
        if rel_path == '.':
            continue

        node_type = rel_path.replace(os.path.sep, '.')

        # A directory is a node if it contains any of the signature files
        is_node = False
        found_params: Dict[str, NodeParameter] = {}
        found_outputs: Dict[str, NodeOutput] = {}

        if "jsonForm.json" in files:
            is_node = True
            for p in extract_params_from_json(os.path.join(root, "jsonForm.json")):
                found_params[p.name] = p

        if "executer.py" in files:
            is_node = True
            params, outputs = extract_params_from_python(os.path.join(root, "executer.py"))
            for p in params:
                if p.name not in found_params:
                    found_params[p.name] = p
            for o in outputs:
                if o.name not in found_outputs:
                    found_outputs[o.name] = o

        # Check for Jinja templates (only legacy jinjaTemplate)
        template_file = None
        if "jinjaTemplate" in files:
            template_file = "jinjaTemplate"

        if template_file:
            is_node = True
            for p in extract_params_from_jinja(os.path.join(root, template_file)):
                if p.name not in found_params:
                    found_params[p.name] = p

        if is_node:
            nodes_info[node_type] = NodeInfo(node_type, list(found_params.values()), list(found_outputs.values()))

    return nodes_info



if __name__ == "__main__":
    results = get_all_node_types()
    for node_type, info in results.items():
        print(f"Node: {node_type}")
        for p in info.parameters:
            print(f"  - (p) {p.name} (req={p.is_required}, src={p.source})")
        for o in info.outputs:
            print(f"  - (o) {o.name} (src={p.source})")
