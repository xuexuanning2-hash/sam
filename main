#!/usr/bin/env python3
"""Sam.test — Psychology Experiment System (Streamlit Web Version)"""

import os
import streamlit as st
from datetime import datetime, timezone
from dotenv import load_dotenv

from config import PROMPTS_DIR, CASE_DIR, ENV_FILE, TOTAL_ROUNDS, GROUPS_WITH_REFLECTION
from participant import get_next_participant_id, assign_group
from data_manager import ensure_data_dir, save_round
from api_client import chat_with_sam

# 页面配置
st.set_page_config(
    page_title="Sam.test - 心理学实验系统",
    page_icon="🎭",
    layout="wide"
)

def load_case() -> str:
    """加载案例文件夹中的所有文件"""
    parts = []
    if CASE_DIR.exists():
        for cf in sorted(CASE_DIR.iterdir()):
            if cf.is_file():
                parts.append(cf.read_text(encoding="utf-8").strip())
    return "\n\n".join(parts)

def load_prompt(group: str) -> str:
    """加载对应实验组的提示词"""
    path = PROMPTS_DIR / f"{group}.txt"
    if not path.exists():
        st.error(f"Missing prompt file: {path}")
        return ""
    return path.read_text(encoding="utf-8").strip()

def init_session_state():
    """初始化 session state"""
    if "initialized" not in st.session_state:
        # 加载环境变量
        load_dotenv(ENV_FILE)
        st.session_state.api_key = os.getenv("DEEPSEEK_API_KEY")
        
        if not st.session_state.api_key:
            st.error("DEEPSEEK_API_KEY not found in environment")
            st.stop()
        
        # 参与者设置
        st.session_state.participant_id = get_next_participant_id()
        st.session_state.group = assign_group()
        st.session_state.system_prompt = load_prompt(st.session_state.group)
        st.session_state.show_reflection = st.session_state.group in GROUPS_WITH_REFLECTION
        
        # 对话状态
        st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]
        st.session_state.round = 1
        st.session_state.conversation_started = False
        st.session_state.initialized = True
        
        # 确保数据目录存在
        ensure_data_dir()
        
        # 显示实验组信息（调试用）
        print(f"Participant: {st.session_state.participant_id}, Group: {st.session_state.group}")

def main():
    init_session_state()
    
    # 侧边栏显示信息
    with st.sidebar:
        st.markdown("### 实验信息")
        st.markdown(f"**参与者ID:** {st.session_state.participant_id}")
        st.markdown(f"**实验组:** {st.session_state.group}")
        st.markdown(f"**当前轮次:** {st.session_state.round}/{TOTAL_ROUNDS}")
        if st.button("重置实验"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # 主标题
    st.title("🎭 Sam.test")
    st.caption("心理学实验系统 | CBT 案例复盘助手")
    
    # 显示案例（只在对话开始前显示）
    if not st.session_state.conversation_started:
        case_content = load_case()
        if case_content:
            with st.expander("📖 案例介绍", expanded=True):
                st.markdown(case_content)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("开始对话", type="primary", use_container_width=True):
                st.session_state.conversation_started = True
                st.rerun()
        return
    
    # 显示对话历史
    st.markdown("### 💬 对话记录")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant", avatar="🎭"):
                st.markdown(msg["content"])
    
    # 用户输入
    if st.session_state.round <= TOTAL_ROUNDS:
        user_input = st.chat_input("请输入你的分析...")
        
        if user_input:
            # 保存用户消息
            now = datetime.now(timezone.utc).isoformat()
            save_round(
                st.session_state.participant_id,
                st.session_state.group,
                st.session_state.round,
                "user",
                user_input,
                now
            )
            
            # 添加到消息历史
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # 调用 API
            with st.spinner("Sam 正在思考..."):
                reflection, response = chat_with_sam(
                    st.session_state.messages,
                    st.session_state.api_key,
                    st.session_state.group
                )
            
            # 显示反思（如果该组需要）
            if reflection and st.session_state.show_reflection:
                with st.expander("🤔 Sam 的思考过程"):
                    st.markdown(reflection)
                save_round(
                    st.session_state.participant_id,
                    st.session_state.group,
                    st.session_state.round,
                    "assistant_reasoning",
                    reflection,
                    now
                )
            
            # 显示回复
            with st.chat_message("assistant", avatar="🎭"):
                st.markdown(response)
            
            # 保存 assistant 回复
            st.session_state.messages.append({"role": "assistant", "content": response})
            save_round(
                st.session_state.participant_id,
                st.session_state.group,
                st.session_state.round,
                "assistant",
                response,
                now
            )
            
            # 评分（第3和6轮后）
            if st.session_state.round in [3, 6]:
                st.markdown("---")
                rating = st.radio(
                    "请评价 Sam 的回答质量（1-5分）",
                    [1, 2, 3, 4, 5],
                    horizontal=True,
                    key=f"rating_{st.session_state.round}"
                )
                if st.button("提交评分", key=f"submit_{st.session_state.round}"):
                    save_round(
                        st.session_state.participant_id,
                        st.session_state.group,
                        st.session_state.round,
                        "rating",
                        str(rating),
                        datetime.now(timezone.utc).isoformat()
                    )
                    st.success("评分已保存")
            
            # 轮次增加
            st.session_state.round += 1
            st.rerun()
    
    # 实验结束
    if st.session_state.round > TOTAL_ROUNDS:
        st.balloons()
        st.success(f"🎉 实验完成！感谢参与。")
        st.markdown(f"**参与者ID:** {st.session_state.participant_id}")
        st.markdown(f"**实验组:** {st.session_state.group}")
        if st.button("重新开始"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()
