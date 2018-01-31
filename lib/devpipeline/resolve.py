#!/usr/bin/python3

def order_dependencies(targets, components):
    counts = {}
    reverse_deps = {}

    def add_reverse_deps(current, deps):
        for dep in deps:
            if dep not in reverse_deps:
                reverse_deps[dep] = [current]
            else:
                reverse_deps[dep].append(current)

    def find_zero_count():
        for key, count in counts.items():
            if count == 0:
                return key
        raise Exception("Resolve error")

    # seed the initial dependencies
    depends = list(targets)
    # build our intermediary objects
    while depends:
        current = depends[0]
        del depends[0]
        # We'll add dependencies in reverse order, so that the original target is built last.
        component = components._components[current]
        if current not in counts:
            current_deps = component._values["depends"]
            add_reverse_deps(current, current_deps)
            counts[current] = len(current_deps)
            depends = depends + current_deps

    ret = []
    while counts:
        key = find_zero_count()
        # key has no deps, so add it
        ret.append(key)
        # reduce remaining dependencies in reverse_deps
        if key in reverse_deps:
            for rev_deps in reverse_deps[key]:
                counts[rev_deps] = counts[rev_deps] - 1
            del reverse_deps[key]
        # delete entry from counts and reverse_deps since it's resolved
        del counts[key]

    return ret
