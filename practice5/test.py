from InvertedIndex import InvertedIndex
import argparse 

def read_file(filename):
    f = open(filename, "r")
    documents = {}
    for line in f.readlines():
        documents[line[:3]] = line[2:]
    f.close()
    return documents

def main():
    parser = argparse.ArgumentParser(description='An example script to check th index')
    parser.add_argument("-t",type=str, required=True,  help="The term to extract")
    args = parser.parse_args()
    index = InvertedIndex()
    documents = read_file("cran-1400.txt")
    print("Initializing index...")
    index.initialize(documents)
    print("Lets check the number of indexed terms:")
    print(str(len(index.terms.keys())))
    print("Checking how many documents contain the word " + args.t)
    try:
        print(len(index.get_post_list(args.t)))
        print("The exact documents are:")
        for doc_id in index.get_post_list(args.t).keys():
            print(doc_id)
    except:
        print("No entry for that term")
        exit(1)


if __name__ == "__main__":
    main()
