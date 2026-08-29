const MARKET_DATA = {

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
};


function getMarkets(){

    return MARKET_DATA;

}


function getMarketCategory(symbol){

    for(const category in MARKET_DATA){

        if(MARKET_DATA[category].includes(symbol)){
            return category;
        }

    }

    return "unknown";
}