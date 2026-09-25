from dataclasses import dataclass, field


@dataclass
class SymbolSnapshot:

    ins_code: str
    isin: str
    symbol: str
    name: str

    market: int = 0
    sector: int = 0

    close: float = 0
    last: float = 0
    first: float = 0
    yesterday: float = 0
    high: float = 0
    low: float = 0

    volume: int = 0
    value: int = 0
    count: int = 0

    buy_volume: int = 0
    sell_volume: int = 0

    buy_count: int = 0
    sell_count: int = 0

    buyer_power: float = 0

    avg_volume: float = 0
    max_volume: float = 0
    volume_ratio: float = 0

    sma55: float = 0

    support: float = 0
    support_volume: int = 0

    resistance: float = 0
    resistance_volume: int = 0

    rr: float = 0
    rr_power: float = 0

    haghighi_buy_average: float = 0

    sarane_average: float = 0

    kh_3_10: float = 0

    sarane3_10: float = 0

    sure10: float = 0

    sureM: float = 0

    money_flow: float = 0

    money_flow_power: float = 0

    unusual_volume: bool = False

    unusual_ratio: float = 0

    smart_money: bool = False

    smart_money_score: int = 0

    smart_money_reason: str = ""

    liquidity_grab: bool = False

    breakout: bool = False

    near_support: bool = False

    near_resistance: bool = False

    uptrend: bool = False

    downtrend: bool = False

    sideway: bool = False

    trend_distance: float = 0

    final_rank: float = 0

    history: list = field(default_factory=list)

    client_history: list = field(default_factory=list)


