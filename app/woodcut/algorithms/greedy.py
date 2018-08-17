from app.woodcut.board import Board



def greedy_algorithm( pieces, material_size ):

    board_collection = []

    # Algorithm

    board_collection.append(Board(material_size))

    pieces.sort(reverse=True)  # sort in ascending order

    def try_placing(piece):
        for board in board_collection:
            if board.space_remaining >= piece:
                board.insert(piece)
                pieces.remove(piece)
                return True
        return False

    for piece in pieces[:]:  # pieces[:] is a copy for the purposes of the algorithm, otherwise our pieces[] would get modified

        #     print ( board_collection[0].contents )
        if try_placing(piece) == True:
            pass
        else:
            board_collection.append(Board(material_size))
            board_collection[-1].insert(piece)
            pieces.remove(piece)


    return str( board_collection )