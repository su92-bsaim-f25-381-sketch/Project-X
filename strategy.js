const PROJECT_X_STRATEGY = {

    name: "Project X Risk Management Strategy",

    mode: "PAPER",

    riskReward: {
        minimum: 2,
        preferred: 3
    },

    indicators: {
        trend: true,
        movingAverage: true,
        RSI: true,
        MACD: true,
        supportResistance: true,
        momentum: true
    },

    analyze: function(data) {

        if (!data) {
            return {
                signal: "WAIT",
                confidence: 0,
                reason: "Market data available nahi hai."
            };
        }

        let score = 0;

        if (data.trend === "BULLISH") {
            score += 2;
        }

        if (data.trend === "BEARISH") {
            score -= 2;
        }

        if (typeof data.rsi === "number") {

            if (data.rsi < 30) {
                score += 1;
            }

            if (data.rsi > 70) {
                score -= 1;
            }
        }

        if (data.macd === "BULLISH") {
            score += 1;
        }

        if (data.macd === "BEARISH") {
            score -= 1;
        }

        let signal = "WAIT";

        if (score >= 3) {
            signal = "BUY";
        } else if (score <= -3) {
            signal = "SELL";
        }

        const confidence = Math.min(
            95,
            50 + Math.abs(score) * 10
        );

        return {
            signal: signal,
            confidence: confidence,
            score: score,
            riskReward: this.riskReward.minimum,
            reason: generateReason(data, signal)
        };
    }
};


function generateReason(data, signal) {

    if (signal === "BUY") {
        return "Bullish conditions detected. Paper-trade setup only.";
    }

    if (signal === "SELL") {
        return "Bearish conditions detected. Paper-trade setup only.";
    }

    return "Conditions are not strong enough. WAIT.";
}


function calculatePositionSize(
    capital,
    riskPercent,
    stopLossDistance,
    pointValue
) {

    if (
        capital <= 0 ||
        riskPercent <= 0 ||
        stopLossDistance <= 0 ||
        pointValue <= 0
    ) {
        return 0;
    }

    const riskAmount =
        capital * (riskPercent / 100);

    const quantity =
        riskAmount /
        (stopLossDistance * pointValue);

    return Math.floor(quantity);
}


function calculateRiskAmount(
    capital,
    riskPercent
) {

    return capital * (riskPercent / 100);
}