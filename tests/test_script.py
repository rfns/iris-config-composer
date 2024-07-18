from icc import Script

def test_writer_input_and_output():
    writer = Script()

    writer.append("test string")
    writer.append("test string 2")

    assert writer.output() == "test string\ntest string 2"

def test_writer_line_count():
    writer = Script()

    writer.append("One")
    writer.append("Two")
    writer.append("Three")

    assert writer.count_lines() == 3
