# Converts collections from Deckbox.org exporting format (csv) to
# Tappedout.in format ("2x Lightning Bolt (M10)"").
# Right now, it only uses the Quantity, Name, Edition, and Foil columns
# of the Deckbox output, but could possibly be changed later.
# The list of set names comes from http://tappedout.net/magic-cards/
# and I had to replace "Magic 2014" with "Magic 2014 Core Set"
# because that's how Deckbox does it. The same may be true with other core
# sets, but I didn't have any of those to test out.

import csv
import sys

data = []

set_names = []

with open("set_names.tsv") as f:
    data_file = csv.reader(f, delimiter="\t")

    for row in data_file:
        set_names.append({"fullname": row[0],
                          "shortname": row[1],
                          "releasedate": row[2]})

def set_name_lookup(fullname):
    answer = [row["shortname"] for row in set_names if row["fullname"] == fullname]
    if len(answer) > 0:
        return answer[0]
    else:
        raise ValueError("Name does not exist")


def create_output(filename, outputname):
    with open(filename) as infile:
        data_file = csv.DictReader(infile)

        for row in data_file:
            data.append(row)

    with open(outputname, "w") as outfile:
        for row in data:
            try:
                set_name = set_name_lookup(row["Edition"])
                outfile.write("{quantity}x {name} ({set})".format(quantity=row["Count"], name=row["Name"], set=set_name_lookup(row["Edition"])))

                if row["Foil"]:
                    outfile.write(" *F*\n")
                else:
                    # have to print new line in both cases
                    outfile.write("\n")
            except ValueError:
                print("Can't find set: {0}".format(row["Edition"]))

# can run as command line script, with argument being filename
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {0} <input_file> [<output_file>]\nUse \"test\" as the argument if you want to see a test".format(sys.argv[0]))
    # check if first argument is test, then execute test
    elif sys.argv[1] == "test":
        create_output("deckbox_collection.csv", "test_output.txt")
    elif len(sys.argv) == 2:
        create_output(sys.argv[1], "tappedout_collection.txt")
    else:
        create_output(sys.argv[1], sys.argv[2])