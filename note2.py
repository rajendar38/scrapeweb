import os
import yaml
from glob import glob

# List of fields to extract per resource kind
FIELD_MAP = {
    "Deployment": ["spec.replicas", "spec.template.spec.containers"],
    "Service": ["spec.type", "spec.ports"],
    "ConfigMap": ["data"],
    "VirtualService": ["spec.hosts", "spec.http"],
}

def extract_field(obj, path):
    keys = path.split(".")
    for key in keys:
        if isinstance(obj, list):
            obj = [item.get(key) for item in obj if item and key in item]
        elif isinstance(obj, dict):
            obj = obj.get(key)
        else:
            return None
    return obj

def extract_values(manifest):
    kind = manifest.get("kind")
    metadata_name = manifest.get("metadata", {}).get("name", "default")
    if kind not in FIELD_MAP:
        return {}

    extracted = {}
    for field_path in FIELD_MAP[kind]:
        val = extract_field(manifest, field_path)
        if val is not None:
            # Simplify container image into repo + tag
            if "containers" in field_path and isinstance(val, list):
                images = val
                extracted["image"] = {}
                for container in images:
                    if container and "image" in container:
                        image_str = container["image"]
                        if ":" in image_str:
                            repo, tag = image_str.split(":", 1)
                        else:
                            repo, tag = image_str, "latest"
                        extracted["image"]["repository"] = repo
                        extracted["image"]["tag"] = tag
            else:
                key = field_path.split(".")[-1]
                extracted[key] = val
    return {kind.lower(): {metadata_name: extracted}}

def load_yaml_documents(file_path):
    with open(file_path, "r") as f:
        return list(yaml.safe_load_all(f))

def collect_manifests(input_path):
    manifests = []
    if os.path.isdir(input_path):
        files = glob(os.path.join(input_path, "*.yaml"))
    else:
        files = [input_path]

    for file in files:
        try:
            docs = load_yaml_documents(file)
            for doc in docs:
                if doc:
                    manifests.append(doc)
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return manifests

def merge_dicts(base, new):
    for key, val in new.items():
        if key not in base:
            base[key] = val
        else:
            base[key].update(val)
    return base

def write_values_yaml(data, output_file="values.yaml"):
    with open(output_file, "w") as f:
        yaml.dump(data, f, sort_keys=False)
    print(f"✅ Generated: {output_file}")

def main(input_path):
    manifests = collect_manifests(input_path)
    values_data = {}
    for manifest in manifests:
        extracted = extract_values(manifest)
        values_data = merge_dicts(values_data, extracted)
    write_values_yaml(values_data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate values.yaml from Kubernetes manifests")
    parser.add_argument("input", help="Path to manifest file or directory")
    args = parser.parse_args()
    main(args.input)