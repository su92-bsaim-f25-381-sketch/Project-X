const TRADING_CONFIG = {
    mode: "PAPER",

    markets: {
        crypto: [
            "BTC/USD",
            "ETH/USD",
            "SOL/USD",
            "XRP/USD",
            "BNB/USD",
            "ADA/USD",
            "DOGE/USD",
            "LTC/USD"
        ],

        forex: [
            "EUR/USD",
            "GBP/USD",
            "USD/JPY",
            "USD/CHF",
            "AUD/USD",
            "USD/CAD",
            "NZD/USD",
            "EUR/GBP",
            "EUR/JPY",
            "GBP/JPY"
        ],

        metals: [
            "XAU/USD",
            "XAG/USD",
            "XPT/USD",
            "XPD/USD"
        ],

        energy: [
            "WTI",
            "BRENT",
            "NATURAL_GAS"
        ],

        indices: [
            "NAS100",
            "US30",
            "SPX500",
            "GER40",
            "UK100"
        ]
    },

    riskManagement: {
        tradingCapitalPercent: 50,
        backupCapitalPercent: 50,
        maxRiskPerTradePercent: 1,
        minimumRiskReward: 2
    },

    analysis: {
        trend: true,
        supportResistance: true,
        movingAverages: true,
        rsi: true,
        macd: true,
        momentum: true,
        volume: true
    }
};