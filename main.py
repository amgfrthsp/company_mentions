import sys
import mentions


def main() -> int:
    pub = mentions.getMentionsByKeywords(["выдры"])
    return 0


if __name__ == '__main__':
    sys.exit(main())
