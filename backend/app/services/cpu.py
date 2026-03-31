from app.services.strategies import RandomStrategy, CustomStrategy, MinimaxStrategy


class EasyCPU(RandomStrategy):
    pass

class MediumCPU(MinimaxStrategy):
    MAX_DEPTH = 2

class HardCPU(CustomStrategy):
    pass

class PerfectCPU(MinimaxStrategy):
    MAX_DEPTH = 9
