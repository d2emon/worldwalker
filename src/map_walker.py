from games.map_walk.windows.map_walk import MapWalkWindow


def main():
    window = MapWalkWindow()
    window.show()
    while window.is_showing:
        window.update()


if __name__ == '__main__':
    main()
