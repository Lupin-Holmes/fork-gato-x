import pytest

from gatox.workflow_graph.node_factory import NodeFactory


@pytest.fixture(autouse=True)
def _empty_node_cache():
    NodeFactory.NODE_CACHE.clear()
    yield
    NodeFactory.NODE_CACHE.clear()


def test_called_workflow_node_workspace_path():
    node = NodeFactory.create_called_workflow_node(
        "./.github/workflows/build.yml", "main", "test/repo"
    )

    assert node.name == "test/repo:main:.github/workflows/build.yml"


def test_called_workflow_node_self_repository_path():
    """A "$/" path names the caller's own repository at the caller's ref."""
    node = NodeFactory.create_called_workflow_node(
        "$/.github/workflows/build.yml", "v2", "test/repo"
    )

    assert node.name == "test/repo:v2:.github/workflows/build.yml"


def test_called_workflow_node_remote_path():
    node = NodeFactory.create_called_workflow_node(
        "other/repo/.github/workflows/build.yml@v1", "main", "test/repo"
    )

    assert node.name == "other/repo:v1:.github/workflows/build.yml"


def test_called_workflow_node_rejects_unknown_format():
    with pytest.raises(ValueError):
        NodeFactory.create_called_workflow_node(
            "other/repo/.github/workflows/build.yml", "main", "test/repo"
        )
