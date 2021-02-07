import os

class Processor:
    def __init__(self, node_coappearance_file_name):
        hyperedge_file_name = "hyperedges.csv"
        print "Processing file " + node_coappearance_file_name
        self.process_node_coappearance_file(node_coappearance_file_name, hyperedge_file_name)

    def dict_to_string(self, D):
        pairs = sorted(D.iteritems(), key = lambda ele: ele[0])
        return ", ".join(map(lambda ele: ele[0].encode("utf-8") + ":" + str(ele[1]), pairs))

    ##read edge file. Each line of the file should be of this format:
    #a,1;b,2;c,3
    #The , is optional in the above line.
    #Each line is read as as dictionary.
    #Different lines may have identical keys, in which case we need to merge these lines.
    #The final result is stored in self.all_node_counts.
    #The keys of self.all_node_counts are the node set, and the values are the merged node_count dictionary.
    def process_node_coappearance_file(self, node_coappearance_file_name, hyperedge_file_name):
        assert(os.path.exists(node_coappearance_file_name))
        self.all_node_counts = dict()
        reader = open(node_coappearance_file_name, "r")
        for (index, string) in enumerate(reader):
            a = string.decode("utf-8").strip("\n").split(", ")
            node_counts = dict()
            for i in range(len(a)):
                b = a[i].split(":")
                if len(b) == 1:
                    weight = 1.0
                else:
                    weight = float(b[1])
                node_counts[b[0]] = weight
            keys = ",".join((sorted(node_counts.keys())))
            if keys in self.all_node_counts:
                self.all_node_counts[keys].append(node_counts)
            else:
                self.all_node_counts[keys] = [node_counts]
        reader.close()

        def merge_node_counts(node_counts_list):
            result = dict()
            for i in range(len(node_counts_list)):
                keys = node_counts_list[i]
                for key in keys:
                    if key in result:
                        result[key] += node_counts_list[i][key]
                    else:
                        result[key] = node_counts_list[i][key]
            return result

        keys = self.all_node_counts.keys()
        for key in keys:
            node_counts_list = self.all_node_counts[key]
            if len(node_counts_list) > 0:
                self.all_node_counts[key] = merge_node_counts(node_counts_list)

        writer = open(hyperedge_file_name, "w")
        keys = self.all_node_counts.keys()
        for key in keys:
            writer.write(self.dict_to_string(self.all_node_counts[key]) + "\n")
        writer.close()


def read_aliases(alias_file_name, character_list_file_name):
    aliases = dict()
    assert(os.path.exists(alias_file_name))
    assert(os.path.exists(character_list_file_name))
    reader = open(alias_file_name, "r")
    for (index, string) in enumerate(reader):
        a = string.strip("\n").decode("utf-8").split(":")
        name = a[0]
        alias_names = a[1].split(",")
        aliases[name] = alias_names
    reader.close()

    reader = open(character_list_file_name, "r")
    for (index, string) in enumerate(reader):
        name = string.strip("\n").decode("utf-8")
        if name in aliases:
            continue
        aliases[name] = []
    reader.close()
    return aliases

def get_scenes(aliases, output_file_name):
    reader = open("content_list.txt", "r")
    content_list = reader.readlines()
    reader.close()
    content_list = map(lambda line: "../data/" + line.strip("\n"), content_list)

    corpus = []
    for i in range(len(content_list)):
        reader = open(content_list[i], "r")
        lines = reader.readlines()
        reader.close()
        corpus += map(lambda line: line.strip("\n").decode("utf-8"), lines)
    
    names = aliases.keys()
    alias_is_subname = dict()
    for name in names:
        alias_names = aliases[name]
        for alias_name in alias_names:
            if alias_name in name:
                alias_is_subname[name] = True
                break
        if name not in alias_is_subname:
            alias_is_subname[name] = False

    def step_function(x):
        if x > 0:
            return 1
        return 0
    scenes = []
    for paragraph in corpus:
        character_appearance_times = dict()
        for name in names:
            if name in paragraph:
                counter = paragraph.count(name)
                if alias_is_subname[name]:
                    counter = 0
                alias_names = aliases[name]
                for alias_name in alias_names:
                    counter += paragraph.count(alias_name)
                character_appearance_times[name] = step_function(counter)
            else:
                alias_names = aliases[name]
                found = False
                for alias_name in alias_names:
                    if alias_name in paragraph:
                        found = True
                        break
                if found:
                    counter = 1
                    for alias_name in alias_names:
                        counter += paragraph.count(alias_name)
                    character_appearance_times[name] = step_function(counter)
        if len(character_appearance_times) > 0:
            scenes.append(character_appearance_times)
            #print paragraph
            #keys = character_appearance_times.keys()
            #for key in keys:
                #print key, character_appearance_times[key]

    writer = open(output_file_name, "w")
    for i in range(len(scenes)):
        scene = scenes[i]
        scene = sorted(scene.iteritems(), key = lambda ele: ele[1], reverse = True)
        scene = map(lambda ele: ele[0] + ":" + str(ele[1]), scene)
        writer.write((", ".join(scene)).encode("utf-8") + "\n")
    writer.close()

def main():
    import sys
    aliases = read_aliases("aliases.txt", "names.txt")
    scene_file_name = "scenes.txt"
    print "Getting node coappearance times ... "
    get_scenes(aliases, scene_file_name)
    print "Generating hyperedges ... "
    processor = Processor(scene_file_name)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
