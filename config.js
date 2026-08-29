const PROJECT_CONFIG = {
    appName: "Project X",

    mode: "PAPER",

    markets: [
        {
            id: "gold",
            name: "Gold",
            symbol: "XAU/USD"
        },
        {
            id: "silver",
            name: "Silver",
            symbol: "XAG/USD"
        },
        {
            id: "oil",
            name: "Crude Oil",
            symbol: "WTI"
        },
        {
            id: "eurusd",
            name: "EUR/USD",
            symbol: "EUR/USD"
        },
        {
            id: "crypto",
            name: "Bitcoin",
            symbol: "BTC/USD"
        }
    ],

    risk: {
        tradingCapitalPercent: 50,
        backupCapitalPercent: 50,
        maxDailyRiskPercent: 1,
        minimumRiskReward: 2
    },

    strategy: {
        trendAnalysis: true,
        supportResistance: true,
        rsi: true,
        macd: true,
        movingAverages: true,
        volumeAnalysis: true,
        momentumAnalysis: true
    }
};