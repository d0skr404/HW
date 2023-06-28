class frange:
    def __init__(self, left, right=None, step=1):
        if right is None:
            left, right = 0, left
        self.left = left
        self.right = right
        self.step = step
        self.comparer = self.left > self.right

    def __next__(self):
        if self.comparer == True:
            if (self.right + self.step >= self.left + self.step) or (self.left > 0 and self.right == 0):
                raise StopIteration
            result = self.left
            if self.step < 0:
                self.left += self.step
            else:
                self.left -= self.step
            return result

        elif self.comparer == False:
            if self.left + self.step >= self.right + self.step:
                raise StopIteration
            result = self.left
            self.left += self.step
            return result

    def __iter__(self):
        return self











