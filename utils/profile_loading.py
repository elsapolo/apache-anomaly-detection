import json

def load_status_profile(path: str) -> dict:
    with open(path, "r") as f:
        raw_profile = json.load(f)

    profile = {}
    for key, inner in raw_profile.items():
        method, path_part = key.split(" ", 1)
        profile[(method, path_part)] = {int(k): v for k, v in inner.items()}

    return profile

def load_query_structure_profile(path: str) -> dict:
    with open(path, "r") as f:
        raw_profile = json.load(f)

    profile = {}
    for method_path, inner in raw_profile.items():
        method, path = method_path.split(" ", 1)
        deserialized = {
            tuple(json.loads(key_str)): freq for key_str, freq in inner.items()
        }
        profile[(method, path)] = deserialized

    return profile