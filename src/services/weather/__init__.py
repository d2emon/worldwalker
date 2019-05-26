class WeatherServices:
    @classmethod
    def get_is_dark(cls, channel):
        def wizard():
            # return __my_lev > 9
            return False

        def room(room_id):
            if room_id == -1100 or room_id == -1101:
                return False
            if channel <= -1113 and room_id >= -1123:
                return True
            if room_id < -399 or room_id > -300:
                return False
            return True

        def lantern():
            # for c in range(__numobs):
            #     if c != 32 and not otstbit(c, 13):
            #         continue
            #     if ishere(c):
            #         return False
            #     if ocarrf(c) in [0, 3]:
            #         continue
            #     if Player.players[GameObject.objects[c].location].location != channel:
            #         continue
            #     return False
            return True

        return (not wizard()) and room(channel) and lantern()
