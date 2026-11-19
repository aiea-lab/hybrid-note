import json
import glob
import re

ALLOWED_NODE_TYPES = {
    "ListNode",
    "OrderedListNode",
    "TaskNode",
    "DateNode",
    "ImportanceNode",
    "EmphasisNode",
    "ContainerNode",
    "ImageNode",
    "MathNode",
    "FocusNode",
    "TableNode",
    "GraphNode"
}

ARRAY_CONTENT_NODE_TYPES = {"ListNode", "OrderedListNode", "TableNode"}

REQUIRED_ELEMNT_FIELDS = {
    "id",
    "type",
    "content",
    "page",
    "location",
    "attributes"
}


def is_redundant_inline_edge(element, relationships):
    attributes = element.get("attributes")
    if element.get("content") is not None or not isinstance(attributes, dict):
        return False

    note = attributes.get("note")
    if not isinstance(note, str):
        return False

    # Older samples describe double-headed arrows in prose alongside their edges.
    endpoints = re.search(
        r"\bdouble-headed arrows? connecting\b.*?\b([\w-]+)\s+and\s+([\w-]+)\.?\s*$",
        note,
        re.IGNORECASE,
    )
    if endpoints is None:
        return False

    source, target = endpoints.groups()
    edge_pairs = [
        (relationship.get("source"), relationship.get("target"))
        for relationship in relationships
        if isinstance(relationship, dict) and relationship.get("type") == "Edge"
    ]
    return source != target and (source, target) in edge_pairs and (target, source) in edge_pairs


def validate_note(file_path, output_path):
    errors = []
    warnings = []

    #load json
    try: 
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"INVALID JSON: {e} ")
        return 
    
    print(f"\nValidating: {file_path}\n")

    #checking top-level structure
    if "document_id" not in data:
        errors.append("Missing 'document_id' field.")
    
    if "elements" not in data or not isinstance(data["elements"], list):
        errors.append("elements must be a list")
    
    if "relationships" not in data or not isinstance(data["relationships"], list):
        errors.append("relationships must be a list")
    
    elements = data.get("elements", [])
    relationships = data.get("relationships", [])

    element_ids = set()
    redundant_edge_ids = set()

    #validating elemnts 
    for element in elements:
        element_id = element.get("id", "UNKNOWN")

        missing = REQUIRED_ELEMNT_FIELDS - set(element.keys())

        if missing: 
            errors.append(
                f"{element_id}: missing fields {sorted(missing)}"
            )

        if element_id in element_ids:
            errors.append(f"Duplicate element id: {element_id}")
        
        element_ids.add(element_id)
        node_type = element.get("type")

        if node_type == "Edge" and is_redundant_inline_edge(element, relationships):
            redundant_edge_ids.add(element_id)
            warnings.append(f"{element_id}: ignored inline Edge already recorded in relationships")
        elif node_type not in ALLOWED_NODE_TYPES:
            errors.append(
                f"{element_id}: invalid node type '{node_type}'")

        content = element.get("content")
        if (
            node_type in ARRAY_CONTENT_NODE_TYPES
            and isinstance(content, list)
            and all(isinstance(item, str) for item in content)
        ):
            content = "\n".join(content)
        if content is not None and not isinstance(content, str):
            errors.append(
                f"{element_id}: content must be a string or null"
            )
        if not isinstance(element.get("attributes"), dict):
            errors.append(
                f"{element_id}: attributes must be an object"
            )
    
    element_ids.difference_update(redundant_edge_ids)

    #validate relationships 
    for i, relationship in enumerate(relationships, start=1):
        if relationship.get("type") != "Edge":
            warnings.append(
                f"Relationship {i}: unexpected type "
                f"'{relationship.get('type')}'"
            )
        
        source = relationship.get("source")
        target = relationship.get("target")

        if source not in element_ids: 
            errors.append(
                f"Relationship {i}: source '{source}' does not exist"
            )
        if target not in element_ids:
            errors.append(
                f"Relationship {i}: target '{target}' does not exist"
            )
    print(f"Document ID: {data.get('document_id')}")
    print(f"Elements detected: {len(elements)}")
    print(f"Relationships detected: {len(relationships)}")


    if errors: 
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("\nNo errors found.")
    
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
    
    #saving
    with open(output_path, "w", encoding="utf-8") as f: 
        f.write(f"Document ID: {data.get('document_id')}\n")
        f.write(f"Elements detected: {len(elements)}\n")
        f.write(f"Relationships detected: {len(relationships)}\n")

        if errors:
            f.write("\nErrors:\n")
            for error in errors:
                f.write(f"- {error}\n")
        else: 
            f.write("\nNo errors found.\n")
        
        if warnings:
            f.write("\nWarnings:\n")
            for warning in warnings:
                f.write(f"- {warning}\n")

    
    print(f"\nValidation summary saved to: {output_path}")

if __name__ == "__main__":
    pages = [10, 11, 12, 13, 14]

    for page in pages: 
        input_file = f"outputs/raw/page_{page}_output.json"
        output_file = f"outputs/validation/page_{page}_validation.txt"

        validate_note(input_file, output_file)
