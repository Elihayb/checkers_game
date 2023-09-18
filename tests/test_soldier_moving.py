def test_move_black_soldier(init_board):
    assert init_board.board[5][0].soldier is not None
    assert init_board.board[4][1].soldier is None
    init_board.move_soldier(old_square=init_board.board[5][0], new_square=init_board.board[4][1])
    assert init_board.board[5][0].soldier is None
    assert init_board.board[4][1].soldier is not None
    assert init_board.board[4][1].soldier.get_location() == init_board.board[4][1].get_location()


def test_move_white_soldier(init_board):
    assert init_board.board[2][1].soldier is not None
    assert init_board.board[3][2].soldier is None
    init_board.move_soldier(old_square=init_board.board[2][1], new_square=init_board.board[3][2])
    assert init_board.board[2][1].soldier is None
    assert init_board.board[3][2].soldier is not None


def test_move_to_far(init_board):
    try:
        init_board.move_soldier(old_square=init_board.board[2][1], new_square=init_board.board[4][2])
    except ValueError as e:
        print(str(e))
    assert init_board.board[2][1].soldier is not None
    assert init_board.board[3][2].soldier is None
    try:
        init_board.move_soldier(old_square=init_board.board[2][1], new_square=init_board.board[3][3])
    except ValueError as e:
        print(str(e))
    assert init_board.board[2][1].soldier is not None
    assert init_board.board[3][2].soldier is None


def test_move_square_without_soldier(init_board):
    try:
        init_board.move_soldier(old_square=init_board.board[3][2], new_square=init_board.board[4][1])
    except ValueError as e:
        print(str(e))
    assert init_board.board[3][2].soldier is None
    assert init_board.board[4][1].soldier is None


def test_move_to_white_square(init_board):
    try:
        init_board.move_soldier(old_square=init_board.board[2][1], new_square=init_board.board[3][1])
    except ValueError as e:
        print(str(e))
    assert init_board.board[2][1].soldier is not None
    assert init_board.board[3][1].soldier is None


def test_move_black_soldier_forward(init_board):
    assert init_board.board[6][1].soldier is not None
    init_board.board[6][1].soldier = None
    assert init_board.board[6][1].soldier is None
    try:
        init_board.move_soldier(old_square=init_board.board[5][0], new_square=init_board.board[6][1])
    except ValueError as e:
        print(str(e))
    assert init_board.board[5][0].soldier is not None
    assert init_board.board[6][1].soldier is None


def test_move_white_soldier_backward(init_board):
    assert init_board.board[1][0].soldier is not None
    init_board.board[1][0].soldier = None
    assert init_board.board[1][0].soldier is None
    try:
        init_board.move_soldier(old_square=init_board.board[2][1], new_square=init_board.board[1][0])
    except ValueError as e:
        print(str(e))
    assert init_board.board[2][1].soldier is not None
    assert init_board.board[1][0].soldier is None


def test_move_soldier_to_occupied_square(init_board):
    try:
        init_board.move_soldier(old_square=init_board.board[1][0], new_square=init_board.board[2][1])
    except ValueError as e:
        print(str(e))
    assert init_board.board[2][1].soldier is not None
    assert init_board.board[1][0].soldier is not None
