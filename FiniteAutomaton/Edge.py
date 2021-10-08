class Edge:
    start: str
    end: str
    value: str

    def __init__(self, start, end, value):
        self.start = str(start)
        self.end = str(end)
        self.value = str(value)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.value == other.value
