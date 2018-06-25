class CyclableList(list):
    _index = 0

    def item_after(self, item, ignore_missing=False):
        try:
            item_index = self.index(item)
        except ValueError:
            if ignore_missing:
                item_index = -1
            else:
                raise

        next_index = item_index + 1
        if next_index >= len(self):
            next_index = 0
        return self[next_index]


    def item_before(self, item, ignore_missing=False):
        try:
            item_index = self.index(item)
        except ValueError:
            if ignore_missing:
                item_index = -1
            else:
                raise

        previous_index = item_index - 1
        if previous_index < 0:
            previous_index = len(self) - 1
        return self[previous_index]

