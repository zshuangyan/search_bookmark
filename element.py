import re


class ElementError(Exception):
    pass


class ElementNameError(ElementError):
    pass


class ElementTypeError(ElementError):
    pass


class ChildNotExist(ElementError):
    pass


class Element:
    RESERVED_REGEXP = re.compile(r"/")

    def __init__(self, name, parent=None, data=None):
        self.name = self.parse_name(name)
        self.parent = parent
        self.data = data
        self.children = []

    def __str__(self):
        return "<name=%s data=%s>" % (self.name, self.data)

    def traverse(self, depth=0):
        logging.info("%s%s" % (' ' * 2 * depth, self))
        for child in self.children:
            child.traverse(depth + 1)

    def get_leaves(self):
        if self.is_leaf:
            return [self]
        results = []
        for child in self.children:
            results.extend(child.get_leaves())
        return results

    @property
    def is_leaf(self):
        return len(self.children) == 0

    @property
    def path(self):
        if not self.parent:
            return "/"
        else:
            return self.parent.path + "/" + self.name

    @classmethod
    def parse_name(cls, name):
        if not isinstance(name, str):
            raise ElementTypeError("请确保名字为字符串类型")
        # 去掉多余的空格
        return re.sub(r"\s+|/", " ", name)

    def add_child(self, child):
        self.children.append(child)
        if not child.parent == self:
            child.parent = self

    def add_children(self, *children):
        for child in children:
            self.add_child(child)

    def remove_child(self, child):
        try:
            self.children.remove(child)
        except Exception:
            raise ChildNotExist("子节点不存在")
        child.parent = None

    def remove_children(self, *children):
        for child in children:
            self.remove_child(child)

    @staticmethod
    def index(elem_list, name):
        for index, elem in enumerate(elem_list):
            if elem.name == name:
                return index
        return -1

    def get_by_path(self, path):
        names = path.split("/")
        current_elem = self
        while names:
            name = names.pop(0)
            index = self.index(current_elem.children, name)
            if index == -1:
                return None
            current_elem = current_elem.children[index]
        return current_elem

    def find_match(self, name, recursive=True):
        def inner(elem):
            if not isinstance(elem, Element):
                raise ElementTypeError("请确保elem参数为Element类型")
            return elem.name == name

        return self._find(self, inner, recursive)

    def find_contain(self, name, recursive=True):
        def inner(elem):
            if not isinstance(elem, Element):
                raise ElementTypeError("请确保elem参数为Element类型")
            return elem.name.find(name) != -1

        return self._find(self, inner, recursive)

    def find_regexp(self, pattern, recursive=True):
        def inner(elem):
            if not isinstance(elem, Element):
                raise ElementTypeError("请确保elem参数为Element类型")
            return re.search(pattern, elem.name)

        return self._find(self, inner, recursive)

    def _find(self, elem, condition_func, recursive):
        results = []
        for child in elem.children:
            if condition_func(child):
                results.append(child)

            child_results = self._find(child, condition_func, recursive)
            if child_results:
                results.extend(child_results)
        return results
