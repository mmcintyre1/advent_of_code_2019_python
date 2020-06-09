from puzzle_input import puzzle_input


def layer_slice(input_str, height, width):
    blocks_per_layer = height * width
    layer_count = len(input_str) // blocks_per_layer
    layer_slices = []

    for i in range(blocks_per_layer):
        layer_row = []
        for j in range(layer_count):
            layer_row.append(input_str[j * blocks_per_layer + i])

        layer_slices.append(layer_row)

    return layer_slices


def main():
    height = 6
    width = 25
    sliced_layers = layer_slice(puzzle_input, height=height, width=width)
    final = []
    for layer in sliced_layers:
        for idx, layer_point in enumerate(layer):
            if idx == len(layer) - 1:
                final.append(layer_point)
            elif layer_point == '2':
                continue
            else:
                final.append(layer_point)
                break

    row_return = 0
    for x in final:
        if row_return == width:
            print()
            row_return = 1
        else:
            row_return += 1
        if x == "1":
            print(int(x), end="")
        else:
            print(" ", end="")


if __name__ == '__main__':
    main()

