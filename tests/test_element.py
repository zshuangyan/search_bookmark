import unittest
from element import Element


class TestElement(unittest.TestCase):
    def test_add_and_remove_child(self):
        root = Element("root")
        assert len(root.children) == 0

        child = Element("child")
        root.add_child(child)
        assert child in root.children
        assert child.parent == root

        root.remove_child(child)
        assert child not in root.children
        assert child.parent is None

    def test_index(self):
        root = Element("root")
        child1 = Element("child1")
        child2 = Element("child2")
        root.add_children(child1, child2)

        assert root.index(root.children, "child1") == 0
        assert root.index(root.children, "child2") == 1
        assert root.index(root.children, "child3") == -1

    def test_get_by_path(self):
        grandpa = Element("grandpa")
        father = Element("father")
        uncle = Element("uncle")
        son = Element("son")
        grandpa.add_children(uncle, father)
        father.add_child(son)

        assert father == grandpa.get_by_path("father")
        assert uncle == grandpa.get_by_path("uncle")
        assert son == grandpa.get_by_path("father/son")

    def test_find_match(self):
        grandpa = Element("grandpa")
        father = Element("father")
        son = Element("son")
        grandpa.add_child(father)
        father.add_child(son)

        assert father == grandpa.find_match("father")[0]
        assert son == grandpa.find_match("son")[0]

    def test_find_contain(self):
        dir1 = Element("dir1")
        file1 = Element("file1")
        file2 = Element("file2")
        dir2 = Element("dir2")
        dir1.add_children(file1, file2, dir2)
        file3 = Element("file3")
        dir2.add_children(file3)

        assert set(dir1.find_contain("file")) == {file1, file2, file3}

    def test_find_regexp(self):
        dir1 = Element("dir1")
        file1 = Element("file1")
        file2 = Element("file2")
        dir2 = Element("dir2")
        dir1.add_children(file1, file2, dir2)
        file3 = Element("file3")
        dir2.add_children(file3)

        assert set(dir1.find_regexp("file.*")) == {file1, file2, file3}


if __name__ == "__main__":
    unittest.main()