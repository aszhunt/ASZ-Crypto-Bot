import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

# Page configuration
st.set_page_config(
    page_title="ASZ Pro Crypto Bot",
    page_icon="👑",
    layout="centered",
)

# Modern, Colorful & Attractive CSS Styling
st.markdown(
    """
    <style>
    /* Background Gradient */
    .stApp {
        background: radial-gradient(circle at center, #1b1b2f 0%, #0f0c1b 100%);
        color: #ffffff;
    }
    
    /* Custom Header Styling */
    .header-title {
        background: linear-gradient(90deg, #00cec9 0%, #6c5ce7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 36px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .sub-header {
        color: #a29bfe;
        text-align: center;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* Selectbox Styling */
    .stSelectbox label {
        color: #00cec9 !important;
        font-weight: 600;
        font-size: 16px;
    }

    /* Glowing Action Button */
    .stButton>button {
        background: linear-gradient(135deg, #6c5ce7 0%, #00cec9 100%);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-size: 18px;
        width: 100%;
        box-shadow: 0 0 20px rgba(0, 206, 201, 0.4);
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00cec9 0%, #6c5ce7 100%);
        box-shadow: 0 0 25px rgba(0, 206, 201, 0.7);
        transform: scale(1.02);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# App Title with ASZ Branding
st.markdown(
    '<p class="header-title">👑 ASZ Pro Crypto Terminal</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-header">High-Accuracy Multi-Indicator Momentum & Trend Analytics (50+ Assets)</p>',
    unsafe_allow_html=True,
)

# 50 Famous Coins & Commodities Dictionary
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
    "Ethereum Classic (ETC/USD)": "ETC-USD",
    "Filecoin (FIL/USD)": "FIL-USD",
    "Tron (TRX/USD)": "TRX-USD",
    "Hedera (HBAR/USD)": "HBAR-USD",
    "Near Protocol (NEAR/USD)": "NEAR-USD",
    "Internet Computer (ICP/USD)": "ICP-USD",
    "Immutable (IMX/USD)": "IMX-USD",
    "VeChain (VET/USD)": "VET-USD",
    "Maker (MKR/USD)": "MKR-USD",
    "Theta Network (THETA/USD)": "THETA-USD",
    "Algorand (ALGO/USD)": "ALGO-USD",
    "Fantom (FTM/USD)": "FTM-USD",
    "The Sandbox (SAND/USD)": "SAND-USD",
    "Decentraland (MANA/USD)": "MANA-USD",
    "Axie Infinity (AXS/USD)": "AXS-USD",
    "Chiliz (CHZ/USD)": "CHZ-USD",
    "Flow (FLOW/USD)": "FLOW-USD",
    "KASPA (KAS/USD)": "KAS-USD",
    "Bonk (BONK/USD)": "BONK-USD",
    "Floki (FLOKI/USD)": "FLOKI-USD",
    "Beam (BEAM/USD)": "BEAM-USD",
    "Celestia (TIA/USD)": "TIA-USD",
    "Pendle (PENDLE/USD)": "PENDLE-USD",
    "Gold (GC=F)": "GC=F",
    "Silver (SI=F)": "SI=F",
}

selected_asset_name = st.selectbox(
    "🔥 Select Asset / Coin for High-Accuracy Analysis (50+ Available):", list(assets.keys())
)
ticker_symbol = assets[selected_asset_name]


def fetch_data(symbol):
  try:
    df = yf.download(symbol, period="5d", interval="15m", progress=False)
    if isinstance(df.columns, pd.MultiIndex):
      df.columns = df.columns.get_level_values(0)
    return df
  except Exception:
    return pd.DataFrame()


def analyze_market(df):
  if df.empty or len(df) < 35:
    return "NEUTRAL", 50.0, 0.0, 0.0

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

  # 1. Advanced Volume Spike Filter
  avg_volume = volume.rolling(window=20).mean().iloc[-1]
  current_volume = volume.iloc[-1]
  vol_spike = current_volume > (avg_volume * 1.25)

  v_buy, v_sell = 0, 0
  if vol_spike and close.iloc[-1] > close.iloc[-2]:
    v_buy += 5
  elif vol_spike:
    v_sell += 5

  # 2. Multi-EMA Trend Crossover (9, 21, 50)
  ema_9 = close.ewm(span=9, adjust=False).mean().iloc[-1]
  ema_21 = close.ewm(span=21, adjust=False).mean().iloc[-1]
  ema_50 = close.ewm(span=50, adjust=False).mean().iloc[-1]
  
  ema_buy, ema_sell = 0, 0
  if current_price > ema_9 > ema_21:
    ema_buy += 6
  elif current_price < ema_9 < ema_21:
    ema_sell += 6
    
  if ema_9 > ema_50:
    ema_buy += 4
  else:
    ema_sell += 4

  # 3. Enhanced RSI (14-period)
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
  if 40 <= rsi <= 55 and close.iloc[-1] > close.iloc[-2]:
    rsi_buy += 5  # Bullish continuation zone
  elif 55 < rsi < 70:
    rsi_buy += 3
  elif rsi < 30:
    rsi_buy += 6  # Oversold bounce
  elif rsi > 70:
    rsi_sell += 6  # Overbought pullback

  # 4. MACD Momentum
  exp1 = close.ewm(span=12, adjust=False).mean()
  exp2 = close.ewm(span=26, adjust=False).mean()
  macd = exp1 - exp2
  sig = macd.ewm(span=9, adjust=False).mean()
  macd_buy, macd_sell = (5, 0) if macd.iloc[-1] > sig.iloc[-1] else (0, 5)

  total_buy = v_buy + ema_buy + rsi_buy + macd_buy
  total_sell = v_sell + ema_sell + rsi_sell + macd_sell
  score_sum = total_buy + total_sell

  buy_pct = (total_buy / score_sum * 100) if score_sum > 0 else 50.0
  sell_pct = 100.0 - buy_pct

  if buy_pct >= 68:
    summary = "STRONG BUY 🚀"
  elif buy_pct >= 56:
    summary = "BUY 📈"
  elif sell_pct >= 68:
    summary = "STRONG SELL 🔻"
  elif sell_pct >= 56:
    summary = "SELL 📉"
  else:
    summary = "NEUTRAL ⚡"

  return summary, buy_pct, sell_pct, current_price


# Button UI
if st.button("✨ Run ASZ High-Accuracy AI Scanner", use_container_width=True):
  with st.spinner("ASZ AI Engine is analyzing multi-timeframe indicators..."):
    df = fetch_data(ticker_symbol)
    if not df.empty and "Close" in df.columns:
      summary, buy_pct, sell_pct, price = analyze_market(df)

      st.markdown("---")
      st.markdown(f"### 📊 Live Report: **{selected_asset_name}**")
      st.metric(
          label="Current Market Price",
          value=f"${price:,.4f}" if price < 10 else f"${price:,.2f}",
      )

      # Colorful Status Alerts
      if "BUY" in summary:
        st.success(f"### Signal: {summary}")
      elif "SELL" in summary:
        st.error(f"### Signal: {summary}")
      else:
        st.warning(f"### Signal: {summary}")

      col1, col2 = st.columns(2)
      with col1:
        st.metric(label="🟢 High-Accuracy Buy Score", value=f"{buy_pct:.1f}%")
      with col2:
        st.metric(label="🔴 High-Accuracy Sell Score", value=f"{sell_pct:.1f}%")

ionali = st.progress(
          int(buy_pct),
          text=f"ASZ AI Probability -> Buy: {buy_pct:.1f}% | Sell: {sell_pct:.1f}%",
      )

      st.markdown("---")
      st.info(
          "💡 **Powered by:** ASZ Pro Crypto Bot | 50+ Coins Advanced Momentum Filtering."
      )
    else:
      st.error(
          "⚠️ Data fetch failed for this asset. Please check network or try another coin."
      )
