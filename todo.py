import streamlit as st

# アプリのタイトル
st.title("ToDoリストアプリ")

# セッションステートにタスクリストを保存
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

# タスクの入力フォーム
new_task = st.text_input("新しいタスクを追加してください:", key="new_task_input")
if st.button("追加"):
    if new_task:
        st.session_state["tasks"].append(new_task)
        st.success(f"タスク '{new_task}' を追加しました！")
    else:
        st.error("タスクを入力してください。")

# タスクリストの表示
if st.session_state["tasks"]:
    st.write("### 現在のタスクリスト:")
    for i, task in enumerate(st.session_state["tasks"]):
        col1, col2 = st.columns([4, 1])
        col1.write(f"- {task}")
        if col2.button("削除", key=f"delete_{i}"):
            # タスクを削除
            del st.session_state["tasks"][i]
            # クエリパラメータをセットしてUIをリフレッシュ
            st.query_params = {"updated": True}
else:
    st.write("タスクリストは空です。")

# フッター
st.write("---")
st.caption("Streamlitで作成された簡単なToDoリストアプリ")
