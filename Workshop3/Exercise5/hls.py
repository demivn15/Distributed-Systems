tree = {
    "ROOT": {
        "AMERICA": {
            "ECUADOR": {
                "IBARRA": {},
                "QUITO": {}
            },
            "USA": {}
        },
        "EUROPE": {}
    }
}

entities = {
    "IBARRA": {
        "server01": "10.0.1.20"
    },
    "QUITO": {
        "server02": "10.0.2.30"
    }
}

# Helper function to find a path from ROOT to any target node in the tree
def find_path_between(current_tree, target, path=None):
    if path is None:
        path = []
    for key, subtree in current_tree.items():
        current_path = path + [key]
        if key == target:
            return current_path
        if isinstance(subtree, dict):
            res = find_path_between(subtree, target, current_path)
            if res:
                return res
    return None

# HLS Lookup implementation: goes up to the Lowest Common Ancestor and down to the target
def lookup(entity, starting_domain):
    # Find which domain currently holds the entity
    target_domain = None
    for dom, store in entities.items():
        if entity in store:
            target_domain = dom
            break
            
    root_to_start = find_path_between(tree, starting_domain)
    
    if not target_domain:
        # If entity doesn't exist anywhere, trace path all the way up to ROOT
        traversal = list(reversed(root_to_start))
        print(" -> ".join(traversal))
        print(f"Entity '{entity}' not found.")
        return None
        
    root_to_target = find_path_between(tree, target_domain)
    
    # Find Lowest Common Ancestor (LCA) index
    lca_idx = 0
    for i in range(min(len(root_to_start), len(root_to_target))):
        if root_to_start[i] == root_to_target[i]:
            lca_idx = i
        else:
            break
            
    # Up path: from starting domain up to LCA
    up_path = list(reversed(root_to_start[lca_idx:]))
    # Down path: from LCA down to target domain (excluding LCA to avoid duplication)
    down_path = root_to_target[lca_idx+1:]
    
    full_path = up_path + down_path + [entity]
    print(" -> ".join(full_path))
    return entities[target_domain][entity]

print("--- HLS Lookups Before Moving ---")
# Test 1: server01 from IBARRA (local lookup)
lookup("server01", "IBARRA")

# Test 2: server02 from IBARRA (upward and downward lookup)
lookup("server02", "IBARRA")

# Test 3: server99 from IBARRA (non-existent entity)
lookup("server99", "IBARRA")

print("\n--- Moving server01 from IBARRA to QUITO ---")
# Update location information in the dictionary
if "server01" in entities["IBARRA"]:
    address = entities["IBARRA"].pop("server01")
    entities["QUITO"]["server01"] = address

# Verify lookup for server01 from IBARRA after it moved
print("Lookup server01 from IBARRA after relocation:")
lookup("server01", "IBARRA")