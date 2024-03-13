import os


def load_yapenv(file=".yapenv"):
    """
    Load environment variables from a file and set them in the os.environ dictionary.

    Args:
        file (str, optional): The path to the file containing environment variables. Defaults to ".yapenv".

    Returns:
        None
    """
    if os.path.exists(file):
        with open(file, "r") as f:
            print("Reading environment variables from {}".format(file))
            for line in f.readlines():
                line = line.strip()
                if not line.strip() or line[0] == '#':
                    continue
                k, v = line.split("=")[:2]
                os.environ[k.strip()] = v.strip()
    else:
        print("Couldn't find environment file {}".format(file))
