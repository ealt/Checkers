import numpy as np

default_board = []
default_board.extend([[-1 for _ in range(4)] for _ in range(3)])
default_board.extend([[ 0 for _ in range(4)] for _ in range(2)])
default_board.extend([[ 1 for _ in range(4)] for _ in range(3)])

line_characters = {
    'horizontal': u'\u2501',
    'vertical': u'\u2503',
    ('top', 'left'): u'\u250F',
    ('top', 'center'): u'\u2533',
    ('top', 'right'): u'\u2513',
    ('middle', 'left'): u'\u2523',
    ('middle', 'center'): u'\u254B',
    ('middle', 'right'): u'\u252B',
    ('bottom', 'left'): u'\u2517',
    ('bottom', 'center'): u'\u253B',
    ('bottom', 'right'): u'\u251B',
}

space_characters = {
    -2: u' \u1E8C ',
    -1: u' X ',
    0: u'   ',
    1: u' O ',
    2: u' \u00D6 ',
    'off': u'   ',

}

def get_column_labels_viz(num_spaces=8, space_width=3):
    return (' ' + ' '.join([' ' + chr(65 + col) + ' '
                            for col in range(num_spaces)]))


def get_horizontal_line_viz(vertical_pos, num_spaces=8, space_width=3):
    return (line_characters[(vertical_pos, 'left')]
            + (space_width * line_characters['horizontal']
                + line_characters[(vertical_pos, 'center')]) * (num_spaces - 1)
            + space_width * line_characters['horizontal']
            + line_characters[(vertical_pos, 'right')])

def get_spaces_viz(identity, row_num):
    if row_num % 2 == 0:
        return (space_characters['off']
                + line_characters['vertical']
                + space_characters[identity])
    else:
        return (space_characters[identity]
                + line_characters['vertical']
                + space_characters['off'])

def get_row_viz(row, row_num, row_label=None):
    return (row_label + ' ' + line_characters['vertical']
            + line_characters['vertical'].join(
                [get_spaces_viz(identity, row_num) for identity in row])
            + line_characters['vertical'] + ' ' + row_label)


def visualize(board):
    num_rows = board.shape[0]
    num_cols = board.shape[1] * 2
    label_w = int(np.floor(np.log10(num_rows))) + 1
    pad = ' ' * label_w
    print(pad, get_column_labels_viz(num_cols))
    print(pad, get_horizontal_line_viz('top', num_cols))
    for row_num, row in enumerate(board):
        row_label = str(num_rows - row_num)
        row_label += ' ' * (label_w - len(row_label))
        print(get_row_viz(row, row_num, row_label))
        if row_num < num_rows-1:
            print(pad, get_horizontal_line_viz('middle', num_cols))
    print(pad, get_horizontal_line_viz('bottom', num_cols))
    print(pad, get_column_labels_viz(num_cols))

def eq(a, b):
    if not (hasattr(a, '__iter__') or type(a) == str):
        return a == b
    try:
        if not len(a) == len(b):
            return False
        elif type(a) == np.ndarray:
            return np.array_equal(a, b)
        elif isinstance(a, dict):
            return all(eq(v, b[k]) for k, v in a.items())
        elif isinstance(a, set):
            return a.symmetric_difference(b) == set()
        else:
            return all(eq(a_i, b_i) for a_i, b_i in zip(a, b))
    except (TypeError, KeyError):
        return False