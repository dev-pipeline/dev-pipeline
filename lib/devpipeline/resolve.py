#!/usr/bin/python3


def _build_dep_data(targets, components):
    counts = {}
    reverse_deps = {}

    def add_reverse_deps(current, deps):
        for dep in deps:
            if dep not in reverse_deps:
                reverse_deps[dep] = [current]
            else:
                reverse_deps[dep].append(current)

    def add_counts(current, counts):
        nonlocal depends
        if current not in counts:
            dep_string = component.get("depends")
            if dep_string:
                current_deps = [x.strip() for x in dep_string.split(",")]
            else:
                current_deps = []
            add_reverse_deps(current, current_deps)
            counts[current] = len(current_deps)
            depends = depends + current_deps

    # seed the initial dependencies
    depends = list(targets)
    # build our intermediary objects
    while depends:
        current = depends[0]
        del depends[0]
        # We'll add dependencies in reverse order, so that the original target
        # is built last.
        component = components[current]
        add_counts(current, counts)

    return (counts, reverse_deps)


def order_dependencies(targets, components):
    def find_zero_count(counts):
        for key, count in counts.items():
            if count == 0:
                return key
        raise Exception("Resolve error")

    def remove_reverse_deps(key, reverse_deps, counts):
        if key in reverse_deps:
            for rev_deps in reverse_deps[key]:
                counts[rev_deps] = counts[rev_deps] - 1
            del reverse_deps[key]

    dep_info = _build_dep_data(targets, components)
    counts = dep_info[0]
    reverse_deps = dep_info[1]
    ret = []
    while counts:
        key = find_zero_count(counts)
        # key has no deps, so add it
        ret.append(key)
        # reduce remaining dependencies in reverse_deps
        # delete entry from counts and reverse_deps since it's resolved
        remove_reverse_deps(key, reverse_deps, counts)
        del counts[key]

    return ret
