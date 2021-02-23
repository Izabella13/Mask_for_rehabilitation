from Psychoemotional_simulator.windows.emotion import Emotion


class Simulator(Emotion):

    def emotion(self, e=1, cmd='sim'):
        if e == 8:
            self.main_window.main__window()
        else:
            if cmd == 'sim':
                self.start(e)
            elif cmd == 'stop':
                self.timer.stop()
                self.emotion(e=e+1)
