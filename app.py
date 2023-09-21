# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
# from streamlit.logger import get_logger

# LOGGER = get_logger(__name__)


def run():
    # アプリのタイトル
    st.title("積立投資シミュレーションアプリ")

    # スライダーを追加
    st.sidebar.header("パラメータ設定")
    years = st.sidebar.slider("想定年数", 1, 30, 10)
    interest_rate = st.sidebar.slider("利回り（年率）", 0.1, 10.0, 2.0, step=0.1)
    monthly_investment = st.sidebar.slider("積立額", 1000, 50000, 20000, step=1000)
    initial_investment = st.sidebar.slider("初期投資額", 10000, 500000, 100000, step=10000)

    # 積み立てシミュレーション
    time_period = np.arange(years + 1)
    investment_values = []
    for year in time_period:
        if year == 0:
            value = initial_investment
        else:
            value = investment_values[-1] * (1 + interest_rate / 100) + monthly_investment * 12
        investment_values.append(value)

    # プロット
    fig, ax = plt.subplots()
    ax.bar(time_period, investment_values, label="最終積立金額", color="blue")
    ax.bar(time_period, np.array(investment_values) - initial_investment, label="増加額", color="green")
    ax.set_xlabel("年数")
    ax.set_ylabel("金額")
    ax.set_title("積立投資シミュレーション")
    ax.legend()

    # グラフを表示
    st.pyplot(fig)



if __name__ == "__main__":
    run()
