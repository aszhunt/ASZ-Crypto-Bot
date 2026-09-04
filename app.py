import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

# Page configuration
st.set_page_config(
    page_title="Pro Crypto & Asset AI Terminal", page_icon="🚀", layout="centered"
)

# Custom High-End Colorful Styling (UI/UX Optimization)
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .stSelectbox label {
        color: #38bdf8 !important;
        font-weight: bold;
        font-size: 16px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 18px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2563eb 100%, #7c3aed 0%);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
        transform: translateY(-2px);
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("💎 Pro AI Multi-Asset Signal Terminal")
st.markdown(
    "<p style='color: #94a3b8;'>Advanced 10-minute momentum and volume AI analysis"
    " engine covering top 30+ Cryptos & Commodities.</p>",
    unsafe_allow_html=True,
)

# 30+ Famous Coins & Assets Dictionary (Yahoo Finance Tickers)
assets = {
    "Bitcoin (BTC/USD)": "BTC-USD",
    "Ethereum (ETH/USD)": "ETH-USD",
    "Solana (SOL/USD)": "SOL-USD",
    "Binance Coin (BNB/USD)": "BNB-USD",
    "Ripple (XRP/USD)": "XRP-USD",
    "Cardano (ADA/USD)": "ADA-USD",
    "Dogecoin (DOGE/USD)": "DOGE-USD",
    "Avalanche (AVAX/USD)": "AVAX-USD",
    "Chainlink (LINK/USD)": "LINK-USD",
    "Polkadot (DOT/USD)": "DOT-USD",
    "Polygon (MATIC/USD)": "MATIC-USD",
    "Litecoin (LTC/USD)": "LTC-USD",
    "Shiba Inu (SHIB/USD)": "SHIB-USD",
    "Uniswap (UNI/USD)": "UNI-USD",
    "Cosmos (ATOM/USD)": "ATOM-USD",
    "Stellar (XLM/USD)": "XLM-USD",
    "Monero (XMR/USD)": "XMR-USD",
    "NEAR Protocol (NEAR/USD)": "NEAR-USD",
    "Aptos (APT/USD)": "APT-USD",
    "Render (RENDER/USD)": "RENDER-USD",
    "Arbitrum (ARB/USD)": "ARB-USD",
    "Optimism (OP/USD)": "OP-USD",
    "Injective (INJ/USD)": "INJ-USD",
    "Sui (SUI/USD)": "SUI-USD",
    "Pepe (PEPE/USD)": "PEPE-USD",
    "Gold (GC=F)": "GC=F",
    "Silver (SI=F)": "SI=F",
    "Ethereum Classic (ETC/USD)": "ETC-USD",
    "Filecoin (FIL/USD)": "FIL-USD",
    "Tron (TRX/USD)": "TRX-USD",
}

selected_asset_name = st.selectbox(
    "🔍 Select Popular Asset/Coin:", list(assets.keys())
)
ticker_symbol = assets[selected_asset_name]


def fetch_data(symbol):
  try:
    df = yf.download(symbol, period="2d", interval="5m", progress=False)
    if isinstance(df.columns, pd.MultiIndex):
      df.columns = df.columns.get_level_values(0)
    return df
  except Exception:
    return pd.DataFrame()


def analyze_market(df):
  if df.empty or len(df) < 30:
    return "NEUTRAL", 50.0, 0, 0, 0, 0.0

  close = df["Close"].squeeze()
  volume = (
      df["Volume"].squeeze()
      if "Volume" in df.columns
      else pd.Series([100] * len(close))
  )

  if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]
  if isinstance(volume, pd.DataFrame):
    volume = volume.iloc[:, 0]

  current_price = float(close.iloc[-1])

  # 1. Volume Factor
  avg_volume = volume.rolling(window=10).mean().iloc[-1]
  current_volume = volume.iloc[-1]
  vol_spike = current_volume > (avg_volume * 1.15)

  v_buy, v_sell = 0, 0
  if vol_spike and close.iloc[-1] > close.iloc[-2]:
    v_buy += 4
  elif vol_spike:
    v_sell += 4

  # 2. EMA Trend (9 & 21)
  ema_9 = close.ewm(span=9, adjust=False).mean().iloc[-1]
  ema_21 = close.ewm(span=21, adjust=False).mean().iloc[-1]
  ema_buy, ema_sell = 0, 0
  if current_price > ema_9:
    ema_buy += 3
  else:
    ema_sell += 3
  if ema_9 > ema_21:
    ema_buy += 3
  else:
    ema_sell += 3

  # 3. RSI Calculation
  delta = close.diff()
  gain = delta.clip(lower=0).rolling(window=14).mean()
  loss = (-delta.clip(upper=0)).rolling(window=14).mean()
  curr_gain = gain.iloc[-1]
  curr_loss = loss.iloc[-1]

  if curr_loss == 0:
    rsi = 100.0
  elif curr_gain == 0:
    rsi = 0.0
  else:
    rsi = 100 - (100 / (1 + (curr_gain / curr_loss)))

  rsi_buy, rsi_sell = 0, 0
  if rsi < 35:
    rsi_buy += 5
  elif rsi > 65:
    rsi_sell += 5
  elif rsi < 50:
    rsi_buy += 2
  else:
    rsi_sell += 2

  # 4. MACD Momentum
  exp1 = close.ewm(span=12, adjust=False).mean()
  exp2 = close.ewm(span=26, adjust=False).mean()
  macd = exp1 - exp2
  sig = macd.ewm(span=9, adjust=False).mean()
  macd_buy, macd_sell = (4, 0) if macd.iloc[-1] > sig.iloc[-1] else (0, 4)

  # Probability breakdown
  total_buy = v_buy + ema_buy + rsi_buy + macd_buy
  total_sell = v_sell + ema_sell + rsi_sell + macd_sell
  score_sum = total_buy + total_sell

  buy_pct = (total_buy / score_sum * 100) if score_sum > 0 else 50.0
  sell_pct = 100.0 - buy_pct

  if buy_pct >= 66:
    summary = "STRONG BUY 🚀"
  elif buy_pct >= 55:
    summary = "BUY 📈"
  elif sell_pct >= 66:
    summary = "STRONG SELL 🔻"
  elif sell_pct >= 55:
    summary = "SELL 📉"
  else:
    summary = "NEUTRAL ⚡"

  return (
      summary,
      buy_pct,
      sell_pct,
      v_buy + v_sell,
      ema_buy + ema_sell + rsi_buy + macd_buy,
      current_price,
  )


# Execution UI Button
if st.button("⚡ Scan Asset & Generate Signal", use_container_width=True):
  with st.spinner("Analyzing live price action, order volumes & indicators..."):
    df = fetch_data(ticker_symbol)
    if not df.empty and "Close" in df.columns:
      summary, buy_pct, sell_pct, v_score, ind_score, price = analyze_market(df)

      st.markdown("---")
      st.markdown(f"### 📊 Live Report: {selected_asset_name}")

      # Gorgeous Metric Container
      st.metric(
          label="Current Market Value",
          value=f"${price:,.4f}" if price < 10 else f"${price:,.2f}",
      )

      # Color-coded Banner Alerts
      if "BUY" in summary:
        st.success(f"### Signal Status: {summary}")
      elif "SELL" in summary:
        st.error(f"### Signal Status: {summary}")
      else:
        st.warning(f"### Signal Status: {summary}")

      # Visual Probability Metric Display
      col1, col2 = st.columns(2)
      with col1:
        st.metric(
            label="🟢 Next 10-Min Buy Chance", value=f"{buy_pct:.1f}%"
        )
      with col2:
        st.metric(
            label="🔴 Next 10-Min Sell Chance", value=f"{sell_pct:.1f}%"
        )

      # Streamlit Progress bar matching probabilities
      st.markdown("**Probability Distribution Bar:**")
      st.progress(
          int(buy_pct),
          text=f"Buy Pressure: {buy_pct:.1f}% | Sell Pressure: {sell_pct:.1f}%",
      )

      st.markdown("---")
      st.info(
          "💡 **Strategy Note:** This engine scans short-term trend momentum"
          " and volume expansion to highlight favorable scalping setups for"
          " the next 10-minute interval."
      )
    else:
      st.error(
          "⚠️ Data fetch failed for this asset. Please try another coin from"
          " the list."
      )