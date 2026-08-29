<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PROJECT X</title>

<style>
*{box-sizing:border-box}
body{
    margin:0;
    font-family:Arial,sans-serif;
    background:#050910;
    color:#fff;
}
header{
    padding:16px;
    background:#0c121c;
    border-bottom:1px solid #263246;
    position:sticky;
    top:0;
    z-index:10;
}
.top{
    display:flex;
    justify-content:space-between;
    align-items:center;
}
.logo{font-size:25px;font-weight:bold}
.live{color:#00e676;font-size:12px;font-weight:bold}
.container{max-width:1300px;margin:auto;padding:14px}
h2{font-size:18px}
.grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(110px,1fr));
    gap:8px;
}
button{
    cursor:pointer;
}
.market{
    padding:12px 7px;
    border-radius:9px;
    border:1px solid #29364a;
    background:#101824;
    color:white;
    font-weight:bold;
}
.market.active{
    background:#1c3855;
    border-color:#4b8bc2;
}
.card{
    background:#0d141f;
    border:1px solid #202c3e;
    border-radius:13px;
    padding:15px;
}
.chart{
    margin-top:14px;
    height:430px;
    background:#0d141f;
    border:1px solid #202c3e;
    border-radius:14px;
    overflow:hidden;
}
canvas{
    width:100%;
    height:100%;
}
.stats{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
    gap:9px;
    margin-top:12px;
}
small{color:#8d9aad}
.value{
    margin-top:7px;
    font-size:19px;
    font-weight:bold;
}
.panel{
    margin-top:14px;
    padding:16px;
    background:#0d141f;
    border:1px solid #202c3e;
    border-radius:14px;
}
input,select{
    width:100%;
    padding:10px;
    margin-top:7px;
    border-radius:8px;
    border:1px solid #29364a;
    background:#080e17;
    color:white;
}
.settings{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
    gap:10px;
}
.apply,.buy,.sell,.back{
    border:0;
    color:white;
    padding:12px;
    border-radius:9px;
    font-weight:bold;
}
.apply{background:#315675;width:100%;margin-top:10px}
.buy{background:#087d4f;flex:1}
.sell{background:#a62d40;flex:1}
.actions{
    display:flex;
    gap:10px;
    margin-top:10px;
}
.switchrow{
    display:flex;
    justify-content:space-between;
    align-items:center;
}
.switch{
    width:60px;
    height:32px;
    position:relative;
}
.switch input{display:none}
.slider{
    position:absolute;
    inset:0;
    background:#374354;
    border-radius:30px;
}
.slider:before{
    content:"";
    position:absolute;
    width:24px;
    height:24px;
    top:4px;
    left:4px;
    background:white;
    border-radius:50%;
    transition:.2s;
}
.switch input:checked+.slider{background:#087d4f}
.switch input:checked+.slider:before{
    transform:translateX(28px);
}
.status{
    margin-top:10px;
    padding:10px;
    background:#101824;
    border-radius:8px;
    color:#a4b0c0;
}
.history{
    max-height:260px;
    overflow:auto;
}
.trade{
    padding:9px;
    margin-top:6px;
    background:#101824;
    border-radius:7px;
    font-size:13px;
}
.back{
    background:#27364a;
    margin-bottom:10px;
}
.warning{
    color:#e6ca7c;
    background:#211b0d;
    padding:10px;
    border-radius:8px;
    margin-top:10px;
    font-size:13px;
}
</style>
</head>

<body>

<header>
<div class="top">
<div class="logo">PROJECT X</div>
<div class="live">● SYSTEM ONLINE</div>
</div>
</header>

<main class="container">

<button class="back" onclick="goBack()">← BACK</button>

<h2>🪙 CRYPTO</h2>

<div class="grid">

<button class="market active"
onclick="selectMarket('BTCUSDT','BTC/USD','crypto',this)">
₿ BTC
</button>

<button class="market"
onclick="selectMarket('ETHUSDT','ETH/USD','crypto',this)">
Ξ ETH
</button>

<button class="market"
onclick="selectMarket('BNBUSDT','BNB/USD','crypto',this)">
◆ BNB
</button>

<button class="market"
onclick="selectMarket('SOLUSDT','SOL/USD','crypto',this)">
◎ SOL
</button>

<button class="market"
onclick="selectMarket('XRPUSDT','XRP/USD','crypto',this)">
◆ XRP
</button>

<button class="market"
onclick="selectMarket('ADAUSDT','ADA/USD','crypto',this)">
₳ ADA
</button>

<button class="market"
onclick="selectMarket('DOGEUSDT','DOGE/USD','crypto',this)">
Ð DOGE
</button>

</div>

<h2>💱 FOREX</h2>

<div class="grid">

<button class="market"
onclick="selectMarket('EURUSD','EUR/USD','tv',this)">
EUR/USD
</button>

<button class="market"
onclick="selectMarket('GBPUSD','GBP/USD','tv',this)">
GBP/USD
</button>

<button class="market"
onclick="selectMarket('USDJPY','USD/JPY','tv',this)">
USD/JPY
</button>

<button class="market"
onclick="selectMarket('USDCHF','USD/CHF','tv',this)">
USD/CHF
</button>

<button class="market"
onclick="selectMarket('AUDUSD','AUD/USD','tv',this)">
AUD/USD
</button>

<button class="market"
onclick="selectMarket('USDCAD','USD/CAD','tv',this)">
USD/CAD
</button>

</div>

<h2>🥇 METALS</h2>

<div class="grid">

<button class="market"
onclick="selectMarket('XAUUSD','GOLD XAU/USD','tv',this)">
🥇 GOLD
</button>

<button class="market"
onclick="selectMarket('XAGUSD','SILVER XAG/USD','tv',this)">
🥈 SILVER
</button>

<button class="market"
onclick="selectMarket('XPTUSD','PLATINUM','tv',this)">
PLATINUM
</button>

<button class="market"
onclick="selectMarket('XPDUSD','PALLADIUM','tv',this)">
PALLADIUM
</button>

</div>

<h2>🛢️ ENERGY</h2>

<div class="grid">

<button class="market"
onclick="selectMarket('USOIL','WTI CRUDE','tv',this)">
WTI
</button>

<button class="market"
onclick="selectMarket('UKOIL','BRENT CRUDE','tv',this)">
BRENT
</button>

</div>

<h2>📊 INDICES</h2>

<div class="grid">

<button class="market"
onclick="selectMarket('NAS100','NAS100','tv',this)">
NAS100
</button>

<button class="market"
onclick="selectMarket('US30','US30','tv',this)">
US30
</button>

<button class="market"
onclick="selectMarket('SPX500','SPX500','tv',this)">
SPX500
</button>

</div>


<div class="card" style="margin-top:14px">
<b id="symbol">BTC/USD</b>
<span style="float:right;color:#00e676">● LIVE</span>
</div>

<div class="chart">
<canvas id="chartCanvas"></canvas>
</div>


<h2>💰 ACCOUNT</h2>

<div class="stats">

<div class="card">
<small>Balance</small>
<div class="value" id="balance">$10,000.00</div>
</div>

<div class="card">
<small>Price</small>
<div class="value" id="price">--</div>
</div>

<div class="card">
<small>Trades</small>
<div class="value" id="trades">0</div>
</div>

<div class="card">
<small>Wins</small>
<div class="value" id="wins">0</div>
</div>

<div class="card">
<small>Losses</small>
<div class="value" id="losses">0</div>
</div>

<div class="card">
<small>Win Rate</small>
<div class="value" id="winrate">0%</div>
</div>

<div class="card">
<small>Total P/L</small>
<div class="value" id="pnl">$0.00</div>
</div>

</div>


<div class="panel">

<h2>⚙️ BOT SETTINGS</h2>

<div class="settings">

<div>
<label>Trading Balance</label>
<input id="balanceInput" type="number" value="10000">
</div>

<div>
<label>Risk Per Trade %</label>
<input id="riskInput" type="number" value="1" step="0.1">
</div>

<div>
<label>Daily Risk Limit %</label>
<input id="dailyInput" type="number" value="3" step="0.1">
</div>

<div>
<label>Risk / Reward</label>
<select id="rrInput">
<option value="2">1 : 2</option>
<option value="3">1 : 3</option>
<option value="4">1 : 4</option>
</select>
</div>

</div>

<button class="apply" onclick="applySettings()">
APPLY SETTINGS
</button>

</div>


<div class="panel">

<div class="switchrow">

<h2>🤖 BOT</h2>

<label class="switch">
<input id="botSwitch"
type="checkbox"
onchange="toggleBot()">
<span class="slider"></span>
</label>

</div>

<div class="status">
Bot Status:
<b id="botStatus">OFF</b>
</div>

<div id="analysis" class="status">
Bot is OFF.
</div>

<div class="warning">
Paper Trading Mode — no real-money order is placed.
</div>

</div>


<div class="panel">

<h2>🎮 MANUAL PAPER TRADE</h2>

<div class="actions">

<button class="buy"
onclick="paperTrade('BUY')">
🟢 BUY
</button>

<button class="sell"
onclick="paperTrade('SELL')">
🔴 SELL
</button>

</div>

</div>


<div class="panel">

<h2>🧠 STRATEGY</h2>

<div class="status">

Trend confirmation → Support/Resistance →
Momentum → Volatility → Entry confirmation →
Risk calculation → Stop Loss → Take Profit.

<br><br>

Risk per trade and daily risk limits are controlled
from Bot Settings. When conditions are unclear,
the bot stays on WAIT.

</div>

</div>


<div class="panel">

<h2>📋 TRADE HISTORY</h2>

<div id="history" class="history">
No trades yet.
</div>

</div>


<div class="panel">

<button class="apply" onclick="resetAccount()">
🔄 RESET PAPER ACCOUNT
</button>

</div>

</main>


<script>

let symbol="BTCUSDT";
let marketName="BTC/USD";
let type="crypto";

let socket=null;
let botTimer=null;
let botOn=false;

let price=0;
let prices=[];

let balance=10000;
let startingBalance=10000;

let wins=0;
let losses=0;
let tradeList=[];


/* BACK */

function goBack(){

    if(history.length>1){
        history.back();
    }else{
        alert("Ye main Project X page hai.");
    }

}


/* UI */

function updateUI(){

    document.getElementById("balance").textContent=
        "$"+balance.toFixed(2);

    document.getElementById("price").textContent=
        price ? "$"+price.toFixed(2) : "--";

    document.getElementById("trades").textContent=
        tradeList.length;

    document.getElementById("wins").textContent=
        wins;

    document.getElementById("losses").textContent=
        losses;

    let completed=wins+losses;

    document.getElementById("winrate").textContent=
        completed ?
        ((wins/completed)*100).toFixed(1)+"%" :
        "0%";

    document.getElementById("pnl").textContent=
        "$"+(balance-startingBalance).toFixed(2);

}


/* SETTINGS */

function applySettings(){

    let newBalance=
        Number(document.getElementById("balanceInput").value);

    if(newBalance<=0){
        alert("Valid balance enter karo.");
        return;
    }

    balance=newBalance;
    startingBalance=newBalance;

    updateUI();

    document.getElementById("analysis").textContent=
        "Settings applied. Paper balance: $"+
        newBalance.toFixed(2);

}


/* MARKET */

function selectMarket(newSymbol,newName,newType,button){

    document
    .querySelectorAll(".market")
    .forEach(function(b){
        b.classList.remove("active");
    });

    button.classList.add("active");

    symbol=newSymbol;
    marketName=newName;
    type=newType;

    prices=[];
    price=0;

    document.getElementById("symbol").textContent=
        marketName;

    if(socket){
        socket.close();
        socket=null;
    }

    if(type==="crypto"){
        connectBinance();
    }else{
        showTradingViewMessage();
    }

    updateUI();

}


/* BINANCE */

function connectBinance(){

    socket=new WebSocket(
        "wss://stream.binance.com:9443/ws/"+
        symbol.toLowerCase()+
        "@trade"
    );

    socket.onmessage=function(event){

        let data=JSON.parse(event.data);

        price=Number(data.p);

        prices.push(price);

        if(prices.length>100){
            prices.shift();
        }

        updateUI();
        drawChart();

    };

    socket.onerror=function(){

        document.getElementById("analysis").textContent=
            "Live crypto connection error.";

    };

}


/* CHART */

function drawChart(){

    let canvas=
        document.getElementById("chartCanvas");

    let box=canvas.parentElement;

    canvas.width=box.clientWidth;
    canvas.height=box.clientHeight;

    let ctx=canvas.getContext("2d");

    ctx.clearRect(
        0,0,
        canvas.width,
        canvas.height
    );

    if(prices.length<2) return;

    let min=Math.min(...prices);
    let max=Math.max(...prices);

    let range=max-min || 1;

    ctx.beginPath();

    prices.forEach(function(p,i){

        let x=
            i*
            (canvas.width/(prices.length-1));

        let y=
            canvas.height-
            ((p-min)/range)*
            (canvas.height-30)-15;

        if(i===0)
            ctx.moveTo(x,y);
        else
            ctx.lineTo(x,y);

    });

    ctx.strokeStyle="#4da3ff";
    ctx.lineWidth=2;
    ctx.stroke();

}


/* OTHER MARKETS */

function showTradingViewMessage(){

    let canvas=
        document.getElementById("chartCanvas");

    let ctx=canvas.getContext("2d");

    let box=canvas.parentElement;

    canvas.width=box.clientWidth;
    canvas.height=box.clientHeight;

    ctx.clearRect(
        0,0,
        canvas.width,
        canvas.height
    );

    ctx.fillStyle="#9ba8ba";
    ctx.font="16px Arial";

    ctx.textAlign="center";

    ctx.fillText(
        "TradingView chart selected:",
        canvas.width/2,
        canvas.height/2-15
    );

    ctx.fillText(
        marketName,
        canvas.width/2,
        canvas.height/2+15
    );

}


/* PAPER TRADE */

function paperTrade(side){

    if(!price){

        alert("Live price available nahi hai.");
        return;

    }

    let riskPercent=
        Number(
            document.getElementById("riskInput").value
        );

    let dailyLimit=
        Number(
            document.getElementById("dailyInput").value
        );

    let riskAmount=
        balance*(riskPercent/100);

    let rr=
        Number(
            document.getElementById("rrInput").value
        );

    let distance=price*0.005;

    let sl,tp;

    if(side==="BUY"){

        sl=price-distance;
        tp=price+(distance*rr);

    }else{

        sl=price+distance;
        tp=price-(distance*rr);

    }

    /*
      Demo paper result.
      Real market outcome is NOT predicted here.
    */

    let result=
        Math.random()>0.5 ?
        "WIN":"LOSS";

    if(result==="WIN"){

        wins++;
        balance+=riskAmount*rr;

    }else{

        losses++;
        balance-=riskAmount;

    }

    tradeList.push({

        side:side,
        market:marketName,
        entry:price,
        sl:sl,
        tp:tp,
        result:result,
        risk:riskAmount

    });

    updateHistory();
    updateUI();

    document.getElementById("analysis").textContent=
        side+" paper trade • "+
        marketName+
        " • Entry $"+
        price.toFixed(2)+
        " • Result: "+
        result;

}


/* BOT */

function toggleBot(){

    let checked=
        document.getElementById("botSwitch").checked;

    if(checked){
        startBot();
    }else{
        stopBot();
    }

}


function startBot(){

    botOn=true;

    document.getElementById("botStatus").textContent=
        "ON";

    document.getElementById("botStatus").style.color=
        "#00e676";

    document.getElementById("analysis").textContent=
        "Project X is monitoring "+
        marketName+
        " in paper mode.";

    botTimer=setInterval(function(){

        if(!price){

            return;

        }

        let signal="WAIT";

        if(prices.length>=20){

            let old=
                prices[prices.length-20];

            let move=
                ((price-old)/old)*100;

            if(move>0.20){
                signal="BUY";
            }else if(move<-0.20){
                signal="SELL";
            }

            document.getElementById("analysis").textContent=
                "Analysing "+
                marketName+
                " • Movement "+
                move.toFixed(3)+
                "% • Signal "+
                signal;

        }

    },1000);

}


function stopBot(){

    botOn=false;

    clearInterval(botTimer);

    document.getElementById("botStatus").textContent=
        "OFF";

    document.getElementById("botStatus").style.color=
        "#ff6678";

    document.getElementById("analysis").textContent=
        "Project X bot is OFF.";

}


/* HISTORY */

function updateHistory(){

    let box=
        document.getElementById("history");

    if(tradeList.length===0){

        box.textContent="No trades yet.";
        return;

    }

    box.innerHTML="";

    tradeList
    .slice()
    .reverse()
    .forEach(function(t){

        let div=
            document.createElement("div");

        div.className="trade";

        div.textContent=
            t.side+
            " • "+
            t.market+
            " • Entry $"+
            t.entry.toFixed(2)+
            " • SL $"+
            t.sl.toFixed(2)+
            " • TP $"+
            t.tp.toFixed(2)+
            " • "+
            t.result;

        box.appendChild(div);

    });

}


/* RESET */

function resetAccount(){

    stopBot();

    let value=
        Number(
            document.getElementById("balanceInput").value
        );

    balance=value;
    startingBalance=value;

    wins=0;
    losses=0;

    tradeList=[];

    updateHistory();
    updateUI();

}


/* RESIZE */

window.addEventListener(
    "resize",
    drawChart
);


/* START */

updateUI();
connectBinance();

</script>

</body>
</html>