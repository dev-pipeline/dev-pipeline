#!/usr/bin/python3
"""Resolve dependencies into an order build list"""


class CircularDependencyException(Exception):
    def __init__(self, circular_components):
        self._components = circular_components

    def __str__(self):
        return "Circular dependency: {}".format(self._components)


def _build_dep_data(targets, components):
    """
    Returns dependency data for a set of targets. An exception will be raised
    if a target does not have component configuration available.
    """
    counts = {}
    reverse_deps = {}

    def _add_reverse_deps(package, dependencies):
        nonlocal reverse_deps

        for dependency in dependencies:
            if dependency not in reverse_deps:
                reverse_deps[dependency] = []
            reverse_deps[dependency].append(package)

    def get_deps_from_component(component):
        """
        Given a component, return a list of dependencies. An empty list will
        be returned for components with no dependencies.
        """
        dependencies = component.get("depends")
        if dependencies:
            return list(x.strip() for x in dependencies.split(','))
        return list()

    # seed the initial dependencies
    to_be_processed = list(targets)
    processed_targets = list()

    missing_components = []
    # populate reverse_deps with who depends on each target
    while to_be_processed:
        current = to_be_processed.pop(0)
        if current in components:
            if current not in processed_targets:
                component_deps = get_deps_from_component(components[current])
                counts[current] = len(component_deps)
                _add_reverse_deps(current, component_deps)

                # process component dependencies as well
                to_be_processed += component_deps
                processed_targets.append(current)
        else:
            missing_components.append(current)

    if missing_components:
        raise Exception(
            "Missing configuration for components: {}".format(
                missing_components))
    return (counts, reverse_deps)


def process_dependencies(targets, components, resolved_fn):
    """
    Given a list of targets and component configurations, return a list of
    targets in build order. The list order guarantees every target's
    dependencies are included prior to that target.

    An exception will be thrown if dependencies can't be resolved.
    """
    def get_resolved_targets(counts):
        """Get a list of targets with a dependency count of 0."""
        resolved_targets = list()
        for target, count in counts.items():
            if count == 0:
                resolved_targets.append(target)

        return resolved_targets

    def remove_reverse_deps(target, reverse_deps, counts):
        """
        Remove a given target from the dependency list of all other targets.
        """
        for rev_deps in reverse_deps[target]:
            counts[rev_deps] -= 1
        del reverse_deps[target]

    counts, reverse_deps = _build_dep_data(targets, components)
    while counts:
        resolved_targets = get_resolved_targets(counts)

        # Every pass must resolve at least one target. An exception is raised
        # if no targets are resolved to avoid an infinte loop.
        if not resolved_targets:
            raise CircularDependencyException(list(reverse_deps.keys()))

        resolved_fn(resolved_targets)

        # cleanup resolved targets
        for target in resolved_targets:
            if target in reverse_deps:
                remove_reverse_deps(target, reverse_deps, counts)
            del counts[target]


def order_dependencies(targets, components):
    target_build_order = []

    def _append_targets(resolved_targets):
        nonlocal target_build_order

        target_build_order += resolved_targets

    process_dependencies(targets, components, _append_targets)
    return target_build_order
