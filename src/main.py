from textnode import *


def main():
    text_node = TextNode("Here is some text", TextType.LINK, "https://www.lit.gov")
    print(text_node)

if __name__ == "__main__":
    main()
