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
    .pred-price { color: #d32f2f; font-size: 1.6rem; font-weight: bold; margin: 10px 0; }
    .pred-diff { font-size: 1.1rem; color: #666; }
    </style>
""", unsafe_allow_html=True)

# --- 2. フォーム ---
st.markdown('<h1 style="color: #ff4b60;">📈 将来価値シミュレーション</h1>', unsafe_allow_html=True)

with st.container():
    mansion_name = st.text_input("マンション名 (任意)", placeholder="例：パークマンション千鳥ヶ淵")
    col1, col2 = st.columns(2)
    with col1:
        # 価格の入力欄を「円」に変更。初期値を1億3752万円に設定。
        price_now = st.number_input("価格 (円)", min_value=1000000, value=137520000, step=1000000) 
        rent_now = st.number_input("賃料 (円)", min_value=1000, value=400000, step=10000)
    with col2:
        area = st.number_input("専有面積 (㎡)", min_value=10.0, value=60.0, step=0.1)
        year_now = st.number_input("築年月 (西暦)", min_value=1970, max_value=2026, value=2015)

st.markdown('<div class="center-container">', unsafe_allow_html=True)
clicked = st.button("　将来価値をシミュレート　")
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. メイン処理 ---
if clicked:
    # 表面利回りの計算 (価格が円単位なので10000倍は不要)
    current_yield = (rent_now * 12) / price_now * 100
    
    def get_prediction(years_later, rate):
        return price_now * (rate ** years_later)

    rates = [1.01, 1.03, 1.05]
    p_5y = [get_prediction(5, r) for r in rates]
    p_10y = [get_prediction(10, r) for r in rates]

    def get_diff_text(future, current):
        diff = round((future/current - 1)*100, 1)
        sign = "+" if diff >= 0 else ""
        return f"{sign}{diff}%"

    st.divider()

    # 価格と利回りを大きく表示（円単位）
    c_base1, c_base2 = st.columns(2)
    with c_base1:
        st.metric("現在のベース価格", f"{int(price_now):,} 円")
    with c_base2:
        st.metric("表面利回り (年間賃料 ÷ 物件価格)", f"{current_yield:.2f}%")

    # 💰 戦略価格パッケージ
    st.markdown(f"""
    ### 💰 戦略価格パッケージ
    | 項目 | 目安金額 | 算出根拠 |
    | :--- | :--- | :--- |
    | 推奨指値 | **{int(price_now):,} 円** | 適正市場価格 |
    | 売出目標 | **{int(price_now*1.15):,} 円** | 強気売出 (+15%) |
    | 下限価格 | **{int(price_now*0.95):,} 円** | 早期売却ライン |
    """)

    # 📅 5年後予測（円単位）
    st.write("### 📅 5年後の市場シナリオ別予測")
    col5_1, col5_2, col5_3 = st.columns(3)
    with col5_1: st.markdown(f'<div class="prediction-card border-light"><div class="pred-label">5年後 (年1%)</div><div class="pred-price">{int(p_5y[0]):,} 円</div><div class="pred-diff">現在比 {get_diff_text(p_5y[0], price_now)}</div></div>', unsafe_allow_html=True)
    with col5_2: st.markdown(f'<div class="prediction-card border-medium"><div class="pred-label">5年後 (年3%)</div><div class="pred-price">{int(p_5y[1]):,} 円</div><div class="pred-diff">現在比 {get_diff_text(p_5y[1], price_now)}</div></div>', unsafe_allow_html=True)
    with col5_3: st.markdown(f'<div class="prediction-card border-heavy"><div class="pred-label">5年後 (年5%)</div><div class="pred-price">{int(p_5y[2]):,} 円</div><div class="pred-diff">現在比 {get_diff_text(p_5y[2], price_now)}</div></div>', unsafe_allow_html=True)

    # 📅 10年後予測（円単位）
    st.write("### 📅 10年後の市場シナリオ別予測")
    col10_1, col10_2, col10_3 = st.columns(3)
    with col10_1: st.markdown(f'<div class="prediction-card border-light"><div class="pred-label">10年後 (年1%)</div><div class="pred-price">{int(p_10y[0]):,} 円</div><div class="pred-diff">現在比 {get_diff_text(p_10y[0], price_now)}</div></div>', unsafe_allow_html=True)
    with col10_2: st.markdown(f'<div class="prediction-card border-medium"><div class="pred-label">10年後 (年3%)</div><div class="pred-price">{int(p_10y[1]):,} 円</div><div class="pred-diff">現在比 {get_diff_text(p_10y[1], price_now)}</div></div>', unsafe_allow_html=True)
    with col10_3: st.markdown(f'<div class="prediction-card border-heavy"><div class="pred-label">10年後 (年5%)</div><div class="pred-price">{int(p_10y[2]):,} 円</div><div class="pred-diff">現在比 {get_diff_text(p_10y[2], price_now)}</div></div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("※2026年時点の統計データに基づく計算シミュレーションです。")
