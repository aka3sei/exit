import streamlit as st
import pandas as pd

# 2026年基準
CURRENT_YEAR = 2026
DEPRECIATION_RATE = 0.008

# --- 1. ページ設定 ---
st.set_page_config(page_title="23区将来価値予測", layout="centered")

st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; display: none; }
    footer { visibility: hidden; }
    .stApp { background: linear-gradient(135deg, #fff5f5 0%, #fff9f0 100%); }
    .center-container { display: flex; justify-content: center; width: 100%; margin: 30px 0; }
    
    .prediction-card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px; text-align: center;
        border: 3px solid;
    }
    .border-light { border-color: #ffdae0 !important; }
    .border-medium { border-color: #ff8fa3 !important; }
    .border-heavy { border-color: #ff4b60 !important; }

    div.stButton > button {
        min-width: 340px !important; height: 60px !important; font-size: 24px !important;
        font-weight: bold !important; background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%) !important;
        color: white !important; border-radius: 40px !important;
        box-shadow: 0 8px 20px rgba(255, 154, 158, 0.3) !important; border: none !important;
    }
    .pred-label { color: #ff758c; font-weight: bold; font-size: 1.1rem; }
    .pred-price { color: #d32f2f; font-size: 2.0rem; font-weight: bold; margin: 10px 0; }
    .pred-diff { font-size: 1.1rem; color: #666; }

    .yield-container {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px; border-radius: 15px;
        border: 2px dashed #ff9a9e; margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. フォーム ---
st.markdown('<h1 style="color: #ff4b60;">📈 将来価値シミュレーション</h1>', unsafe_allow_html=True)
st.subheader("〜 市場上昇シナリオ別の予測 〜")

with st.container():
    mansion_name = st.text_input("マンション名 (任意)", placeholder="例：パークマンション千鳥ヶ淵")
    col1, col2 = st.columns(2)
    with col1:
        price_now = st.number_input("価格 (万円)", min_value=1, value=8000)
        rent_now = st.number_input("賃料 (円)", min_value=1, value=250000)
    with col2:
        area = st.number_input("専有面積 (㎡)", min_value=1.0, value=60.0)
        year_now = st.number_input("築年月 (西暦)", min_value=1970, max_value=2026, value=2015)

st.markdown('<div class="center-container">', unsafe_allow_html=True)
clicked = st.button("　将来価値をシミュレート　")
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. メイン処理 ---
if clicked:
    # --- 計算開始 ---
    # 利回り計算 (1万円単位を補正)
    current_yield = (rent_now * 12) / (price_now * 10000) * 100

    def get_prediction(years_later, rate):
        return price_now * (rate ** years_later)

    def calc_f_rent(base, yrs, infl):
        return base * ((1 - DEPRECIATION_RATE)**yrs) * ((1 + infl)**yrs)

    # 市場上昇率ごとの計算
    rates = [1.01, 1.03, 1.05]
    p_5y = [get_prediction(5, r) for r in rates]
    p_10y = [get_prediction(10, r) for r in rates]
    
    # 賃料将来計算（市場上昇の半分がインフレと仮定）
    r_10y = [calc_f_rent(rent_now, 10, (r-1)/2) for r in rates]
    y_10y = [(r * 12) / (p * 10000) * 100 for r, p in zip(r_10y, p_10y)]

    def get_diff_text(future, current):
        diff = round((future/current - 1)*100, 1)
        sign = "+" if diff >= 0 else ""
        return f"{sign}{diff}%" # カッコを排除

    st.divider()

    # 💰 収益性・利回りシミュレーション
    st.markdown('<div class="yield-container">', unsafe_allow_html=True)
    st.write("### 💰 収益性・利回りシミュレーション")
    y_col1, y_col2, y_col3, y_col4 = st.columns(4)
    y_col1.metric("現在の利回り", f"{current_yield:.2f}%")
    y_col2.metric("10年後 1%時", f"{y_10y[0]:.2f}%")
    y_col3.metric("10年後 3%時", f"{y_10y[1]:.2f}%")
    y_col4.metric("10年後 5%時", f"{y_10y[2]:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

    # 💰 戦略価格パッケージ
    st.markdown(f"""
    ### 💰 戦略価格パッケージ
    | 項目 | 目安金額 | 算出根拠 |
    | :--- | :--- | :--- |
    | 推奨指値 | **{round(price_now):,} 万円** | 適正市場価格 |
    | 売出目標 | **{round(price_now*1.15):,} 万円** | 強気売出 (+15%) |
    | 下限価格 | **{round(price_now*0.95):,} 万円** | 早期売却ライン |
    """)

    # 📅 5年後の市場シナリオ別予測
    st.write("### 📅 5年後の市場シナリオ別予測")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="prediction-card border-light"><div class="pred-label">5年後 (年1%)</div><div class="pred-price">{round(p_5y[0]):,}</div><div class="pred-diff">現在比 {get_diff_text(p_5y[0], price_now)}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="prediction-card border-medium"><div class="pred-label">5年後 (年3%)</div><div class="pred-price">{round(p_5y[1]):,}</div><div class="pred-diff">現在比 {get_diff_text(p_5y[1], price_now)}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="prediction-card border-heavy"><div class="pred-label">5年後 (年5%)</div><div class="pred-price">{round(p_5y[2]):,}</div><div class="pred-diff">現在比 {get_diff_text(p_5y[2], price_now)}</div></div>', unsafe_allow_html=True)

    # 📅 10年後の市場シナリオ別予測
    st.write("### 📅 10年後の市場シナリオ別予測")
    c4, c5, c6 = st.columns(3)
    with c4: st.markdown(f'<div class="prediction-card border-light"><div class="pred-label">10年後 (年1%)</div><div class="pred-price">{round(p_10y[0]):,}</div><div class="pred-diff">現在比 {get_diff_text(p_10y[0], price_now)}</div></div>', unsafe_allow_html=True)
    with c5: st.markdown(f'<div class="prediction-card border-medium"><div class="pred-label">10年後 (年3%)</div><div class="pred-price">{round(p_10y[1]):,}</div><div class="pred-diff">現在比 {get_diff_text(p_10y[1], price_now)}</div></div>', unsafe_allow_html=True)
    with c6: st.markdown(f'<div class="prediction-card border-heavy"><div class="pred-label">10年後 (年5%)</div><div class="pred-price">{round(p_10y[2]):,}</div><div class="pred-diff">現在比 {get_diff_text(p_10y[2], price_now)}</div></div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("※2026年時点の統計データに基づく計算シミュレーションです。")
