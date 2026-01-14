import streamlit as st
import pandas as pd

# 2026年基準
CURRENT_YEAR = 2026
DEPRECIATION_RATE = 0.008  # 建物老朽化による賃料下落率 (年0.8%)

# --- 1. ページ設定 ---
st.set_page_config(page_title="未来資産シミュレーター", layout="centered")

# ハッピーな色の設定 (ピンク、オレンジ、明るい青のグラデーション)
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; display: none; }
    footer { visibility: hidden; }
    /* 背景を明るいパステル調に */
    .stApp { background: linear-gradient(135deg, #fff5f5 0%, #fff9f0 100%); }
    
    .center-container { display: flex; justify-content: center; width: 100%; margin: 30px 0; }
    
    /* ボタンをハッピーなオレンジグラデーションに */
    div.stButton > button {
        min-width: 340px !important; height: 60px !important; font-size: 24px !important;
        font-weight: bold !important; background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%) !important;
        color: #fff !important; border-radius: 40px !important;
        box-shadow: 0 8px 20px rgba(255, 154, 158, 0.4) !important; border: none !important;
    }
    
    /* カードのデザインを丸く、明るく */
    .prediction-card {
        background: white; padding: 25px; border-radius: 20px;
        border: 2px solid #ffe4e6; box-shadow: 0 10px 25px rgba(255,182,193,0.1);
        margin-bottom: 25px; text-align: center;
    }
    .pred-label { color: #ff758c; font-weight: bold; font-size: 1.0rem; }
    .pred-price { color: #d32f2f; font-size: 2.2rem; font-weight: bold; margin: 8px 0; }
    .pred-diff { font-size: 1.1rem; }
    
    /* 入力エリアの背景 */
    [data-testid="stVerticalBlock"] > div:has(input) {
        background-color: rgba(255, 255, 255, 0.6);
        border-radius: 15px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. フォーム ---
st.markdown('<h1 style="text-align: center; color: #ff4b60;">✨ 未来価値シミュレーション</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #ff758c;">〜 大切な資産の10年後を描いてみましょう 〜</p>', unsafe_allow_html=True)

with st.container():
    mansion_name = st.text_input("物件名", placeholder="例：素敵なマイホーム")
    
    col1, col2 = st.columns(2)
    with col1:
        price_now = st.number_input("現在の価格 (万円)", min_value=100, value=8000, step=100)
        rent_now = st.number_input("現在の賃料 (円)", min_value=1000, value=250000, step=1000)
    with col2:
        area = st.number_input("専有面積 (㎡)", min_value=10.0, value=60.0, step=0.1)
        year_built = st.number_input("築年 (西暦)", min_value=1970, max_value=2026, value=2015)

st.markdown('<div class="center-container">', unsafe_allow_html=True)
clicked = st.button("　未来をシミュレートする　")
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. 計算と表示 ---
if clicked:
    yield_now = (rent_now * 12) / (price_now * 10000) * 100

    def calc_future_price(years, market_growth_rate):
        return price_now * ((1 + market_growth_rate) ** years)

    p_5y = [calc_future_price(5, r) for r in [0.01, 0.03, 0.05]]
    p_10y = [calc_future_price(10, r) for r in [0.01, 0.03, 0.05]]

    def get_diff_html(future, current):
        diff = round((future / current - 1) * 100, 1)
        color = "#ff4b60" if diff >= 0 else "#3b82f6"
        sign = "+" if diff >= 0 else ""
        return f'<span style="color: {color}; font-weight: bold;">{sign}{diff}%</span>'

    st.divider()
    
    # 基本メトリクス
    c1, c2, c3 = st.columns(3)
    c1.metric("想定利回り", f"{yield_now:.2f} %")
    c2.metric("平米価格", f"{int(price_now / area):,} 万円/㎡")
    c3.metric("賃料単価", f"{int(rent_now / area):,} 円/㎡")

    # 5年後シナリオ
    st.markdown('<h3 style="color: #ff758c;">🌈 5年後のHAPPYな予測</h3>', unsafe_allow_html=True)
    cols_5 = st.columns(3)
    labels = ["ゆっくり (年1%)", "たのしみ (年3%)", "わくわく (年5%)"]
    for i, col in enumerate(cols_5):
        with col:
            st.markdown(f'''
                <div class="prediction-card" style="border-top: 6px solid #ff9a9e;">
                    <div class="pred-label">{labels[i]}</div>
                    <div class="pred-price">{int(p_5y[i]):,} 万円</div>
                    <div class="pred-diff">期待値 {get_diff_html(p_5y[i], price_now)}</div>
                </div>
            ''', unsafe_allow_html=True)

    # 10年後シナリオ
    st.markdown('<h3 style="color: #ff758c;">🌟 10年後の未来予測</h3>', unsafe_allow_html=True)
    cols_10 = st.columns(3)
    for i, col in enumerate(cols_10):
        with col:
            st.markdown(f'''
                <div class="prediction-card" style="border-top: 6px solid #fda085;">
                    <div class="pred-label">{labels[i]}</div>
                    <div class="pred-price">{int(p_10y[i]):,} 万円</div>
                    <div class="pred-diff">期待値 {get_diff_html(p_10y[i], price_now)}</div>
                </div>
            ''', unsafe_allow_html=True)

    # 賃料
    st.write("---")
    st.markdown('<h3 style="color: #ff758c;">🏠 賃料の将来予測</h3>', unsafe_allow_html=True)
    
    def calc_future_rent(years, inflation_rate):
        return rent_now * ((1 - DEPRECIATION_RATE)**years) * ((1 + inflation_rate)**years)

    r10_1 = calc_future_rent(10, 0.01)
    r10_2 = calc_future_rent(10, 0.02)

    rc1, rc2, rc3 = st.columns(3)
    rc1.metric("現在の賃料", f"{int(rent_now):,} 円")
    rc2.metric("10年後 (インフレ1%)", f"{int(r10_1):,} 円")
    rc3.metric("10年後 (インフレ2%)", f"{int(r10_2):,} 円")

st.markdown("---")
st.caption("※このシミュレーションは入力された数値に基づく計算モデルであり、将来の価値を約束するものではありません。")
