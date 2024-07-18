class Script:
    def __init__(self):
        self._buffer: list[str] = []

    def append(self, line: str) -> None:
        """
        Inserts a new line into the buffer.
        """
        self._buffer.append(line)

    def output(self) -> str:
        """
        Output the current buffer to the stdout.
        """
        return "\n".join(self._buffer)

    def count_lines(self) -> int:
        "Count the number of lines already in the buffer."
        return len(self._buffer)
