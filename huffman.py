import heapq
from collections import Counter


class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:

    def __init__(self):
        self.root = None
        self.codes = {}
        self.reverse_codes = {}

    # Build Huffman Tree
    def build_tree(self, text):
        frequency = Counter(text)

        heap = []
        for char, freq in frequency.items():
            heapq.heappush(heap, Node(char, freq))

        # Only one unique character
        if len(heap) == 1:
            self.root = heap[0]
            self.codes[heap[0].char] = "0"
            self.reverse_codes["0"] = heap[0].char
            return

        # Greedy algorithm
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            new_node = Node(freq=left.freq + right.freq)
            new_node.left = left
            new_node.right = right

            heapq.heappush(heap, new_node)

        self.root = heap[0]

        # Generate codes
        self.generate_codes(self.root, "")

    # Generate Huffman codes
    def generate_codes(self, node, code):
        if node is None:
            return

        if node.char is not None:
            self.codes[node.char] = code
            self.reverse_codes[code] = node.char
            return

        self.generate_codes(node.left, code + "0")
        self.generate_codes(node.right, code + "1")

    # Encode text
    def encode(self, text):
        return "".join(self.codes[char] for char in text)

    # Decode binary string
    def decode(self, encoded):
        if not encoded:
            return ""

        result = []
        node = self.root

        # Single character case
        if node.left is None and node.right is None:
            return node.char * len(encoded)

        for bit in encoded:
            if bit == "0":
                node = node.left
            else:
                node = node.right

            if node.char is not None:
                result.append(node.char)
                node = self.root

        return "".join(result)

    # Calculate tree statistics
    def tree_statistics(self):
        def calculate(node, depth=0):
            if node is None:
                return 0, 0, 0

            if node.char is not None:
                return 1, 1, depth

            left_nodes, left_leaves, left_height = calculate(
                node.left, depth + 1
            )
            right_nodes, right_leaves, right_height = calculate(
                node.right, depth + 1
            )

            return (
                1 + left_nodes + right_nodes,
                left_leaves + right_leaves,
                max(left_height, right_height)
            )

        nodes, leaves, height = calculate(self.root)

        return nodes, leaves, height


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("          HUFFMAN COMPRESSION UTILITY")
    print("=" * 60)

    text = input("\nEnter text to compress: ")

    if not text:
        print("Please enter some text.")
        return

    huffman = HuffmanCoding()

    # Build Huffman tree
    huffman.build_tree(text)

    # Encode
    encoded = huffman.encode(text)

    # Decode
    decoded = huffman.decode(encoded)

    # Tree statistics
    nodes, leaves, height = huffman.tree_statistics()

    # Original size
    original_bits = len(text.encode("utf-8")) * 8

    # Compressed size
    compressed_bits = len(encoded)

    # Compression ratio
    if compressed_bits > 0:
        compression_ratio = original_bits / compressed_bits
    else:
        compression_ratio = 0

    # Space saving
    if original_bits > 0:
        space_saving = (
            (original_bits - compressed_bits)
            / original_bits
        ) * 100
    else:
        space_saving = 0

    # Fixed-length comparison
    unique_chars = len(set(text))

    if unique_chars <= 1:
        fixed_bits_per_char = 1
    else:
        fixed_bits_per_char = (unique_chars - 1).bit_length()

    fixed_length_bits = len(text) * fixed_bits_per_char

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    print("\n" + "-" * 60)
    print("HUFFMAN CODES")
    print("-" * 60)

    for char, code in sorted(
        huffman.codes.items(),
        key=lambda x: x[1]
    ):
        if char == " ":
            display = "SPACE"
        elif char == "\n":
            display = "NEWLINE"
        elif char == "\t":
            display = "TAB"
        else:
            display = char

        print(f"{display:10} -> {code}")

    print("\n" + "-" * 60)
    print("ENCODED TEXT")
    print("-" * 60)
    print(encoded)

    print("\n" + "-" * 60)
    print("DECODED TEXT")
    print("-" * 60)
    print(decoded)

    print("\nDecoding correct:", decoded == text)

    print("\n" + "-" * 60)
    print("TREE STATISTICS")
    print("-" * 60)

    print("Unique characters :", len(set(text)))
    print("Total tree nodes  :", nodes)
    print("Leaf nodes        :", leaves)
    print("Tree height       :", height)

    print("\n" + "-" * 60)
    print("COMPRESSION RESULTS")
    print("-" * 60)

    print("Original size     :", original_bits, "bits")
    print("Compressed size   :", compressed_bits, "bits")
    print(f"Compression ratio : {compression_ratio:.2f}:1")
    print(f"Space saved       : {space_saving:.2f}%")

    print("\n" + "-" * 60)
    print("ALGORITHM COMPARISON")
    print("-" * 60)

    print(
        "Fixed-length encoding :",
        fixed_length_bits,
        "bits"
    )

    print(
        "Huffman encoding      :",
        compressed_bits,
        "bits"
    )

    if fixed_length_bits > 0:
        improvement = (
            (fixed_length_bits - compressed_bits)
            / fixed_length_bits
        ) * 100

        print(
            f"Reduction compared to fixed-length : "
            f"{improvement:.2f}%"
        )

    print("\n" + "=" * 60)
    print("              COMPRESSION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
