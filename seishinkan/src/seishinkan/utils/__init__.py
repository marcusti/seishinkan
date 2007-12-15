class XFieldList(list):
    """ List for field names.
    Changes "*_" to specific field names for the current language,
    i.e.
    "sort_order" => "sort_order"
    "title_" => "title", "title_de", or "title_es"
    "__str__" => "__str__"
    """
    def __init__(self, sequence=[]):
        self.sequence = sequence
    def __iter__(self):
        return iter(self._get_list())
    def __getitem__(self, k):
        return self._get_list()[k]
    def __nonzero__(self):
        return bool(self.sequence)
    def __len__(self):
        return len(self.sequence)
    def __str__(self):
        return str(self._get_list())
    def __repr__(self):
        return repr(self._get_list())
    def _get_list(self):
        language = translation.get_language()[:2]
        result = []
        for item in self.sequence:
            if item[:1]=="-":
                order = "-"
                item = item[1:]
            else:
                order = ""
            if item[:2] == "__" or item[-1:] != "_":
                result.append(order + item)
            else:
                if language == "de":
                    result.append(order + item[:-1])
                else:
                    result.append(order + item + language)
        return result

