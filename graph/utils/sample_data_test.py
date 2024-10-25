from . import sample_data as sd

if __name__ == "__main__":
    graph = sd.read_from_file()
    if graph == None:
        graph = sd.generate_sample_data()
        sd.write_to_file(graph)
