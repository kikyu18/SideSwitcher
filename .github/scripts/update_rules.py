import os
import sys
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
issue_body = os.environ.get("ISSUE_BODY", "")
html_file_path = "index.html"  # リポジトリ内のHTMLファイル名に合わせて変更

if not issue_body.strip():
    print("Issue本文が空のため処理を中断します。")
    sys.exit(0)

# 既存のHTMLを読み込み
current_html = ""
if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        current_html = f.read()

# 最新SDKでのクライアント初期化
client = genai.Client(api_key=api_key)

prompt = f"""
あなたはボードゲームのルール説明用Webページのデザイナー兼エンジニアです。

【既存のHTML】
{current_html}

【変更・追加したいルール内容】
{issue_body}

【指示】
既存のHTMLのデザイン・CSS構造・世界観を完全に維持したまま、上記の「変更・追加したいルール内容」を適切に反映した完全なHTMLファイルを生成してください。
出力はMarkdownのコードブロック（```html ... ```）を一切含めず、<!DOCTYPE html>から始まる純粋なHTML文字列のみを出力してください。
"""

# 最新の推奨モデルを指定
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

updated_html = response.text.strip()

# マークダウン記号が混入した場合のトリミング
if updated_html.startswith("```html"):
    updated_html = updated_html[7:]
if updated_html.startswith("```"):
    updated_html = updated_html[3:]
if updated_html.endswith("```"):
    updated_html = updated_html[:-3]
updated_html = updated_html.strip()

with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(updated_html)

print("HTMLファイルの更新が完了しました。")
