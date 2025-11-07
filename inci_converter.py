#!/usr/bin/env python
# coding: utf-8

# In[58]:


import csv # csvファイルの読み書き
import os  # osの操作
import re  # 正規表現

# データ読み込み、エラーハンドリング
def load_inci_data(filename='inci_map.csv'):

    # 空の辞書
    inci_to_jp = {} 
    jp_to_inci = {} 
    
    # ファイルの存在確認
    if not os.path.exists(filename):
        print(f"❌ 致命的なエラー：ファイル '{filename}' が指定されたパスに見つかりません。")
        return ({}, {}) # 空のタプル

    try:
        # 1. UTF-8で試行
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None) # ヘッダー行を読み飛ばす

            for row in reader:
                if len(row) == 2:
                    # .strip()で前後の不要な空白を削除
                    inci_name = row[0].strip()
                    jp_name = row[1].strip()

                    # .lower()で小文字にして格納
                    inci_to_jp[inci_name.lower()] = jp_name
                    jp_to_inci[jp_name.lower()] = inci_name

            return (inci_to_jp, jp_to_inci) 

    except UnicodeDecodeError:
        print("⚠️ 警告: UTF-8での読み込みに失敗しました。Shift-JISで再試行します。")
        
        # 辞書を一度空にする
        inci_to_jp = {}
        jp_to_inci = {}
        
        try: # Shift-JISでの再試行を開始
            with open(filename, mode='r', encoding='shift_jis') as file:
                reader = csv.reader(file)
                next(reader, None)
                
                for row in reader:
                    if len(row) == 2:
                        inci_name = row[0].strip()
                        jp_name = row[1].strip()
                        inci_to_jp[inci_name.lower()] = jp_name
                        jp_to_inci[jp_name.lower()] = inci_name
                        
            return (inci_to_jp, jp_to_inci)
        
        except Exception as e:
            print(f"❌ 致命的なエラー（Shift-JIS試行失敗）: {e}")
            return ({}, {})

# あいまい検索
def fuzzy_convert_ingredient(name, inci_to_jp_map, jp_to_inci_map):

    search_key = name.strip().lower() # 小文字化、空白除去

    results = [] # 空のリスト

    pattern = re.compile(f".*{re.escape(search_key)}.*") # 特殊文字を無効化

    # INCI名 -> 日本語名
    for inci_name_key, jp_name_value in inci_to_jp_map.items():
        if pattern.match(inci_name_key):
            results.append(f"INCI名 (部分一致): {inci_name_key} -> 日本語名: {jp_name_value}")
            
    # 日本語名 -> INCI名
    for jp_name_key, inci_name_value in jp_to_inci_map.items():
        if pattern.match(jp_name_key):
            results.append(f"日本語名 (部分一致): {jp_name_key} -> INCI名: {inci_name_value}")
            
    # 結果の返却
    if results:
        return "\n".join(results) # 見つかった全ての候補を改行で区切って返す
    else:
        return f"❌ 「{name}」の部分一致する成分は見つかりませんでした。"

# コマンドラインインターフェース
def main():
    
    file_path = '/Users/user/Desktop/Python開発/INCI Translator/inci_map.csv' 
    
    # データを読み込む
    inci_jp_map, jp_inci_map = load_inci_data(filename=file_path)

    # 読み込み失敗時は終了
    if not inci_jp_map:
        print("プログラムを終了します。データファイルのパスを確認してください。")
        return # 関数を終了

    print("\n-----------------------------------------------------------")
    print("✨ INCI Translator CLI ✨")
    print(f"成分データベース読み込み完了。合計 {len(inci_jp_map)} 件")
    print("-----------------------------------------------------------")

    # 無限ループでユーザーからの入力を待ち受ける
    while True:
        # ユーザーに入力を促す
        ingredient_input = input("\n成分名を入力してください (例: Water, グリセリン) または 'end' で終了: ")
        
        # 終了コマンドチェック
        if ingredient_input.lower() == 'end':
            print("INCI Translator を終了します。ご利用ありがとうございました。")
            break # ループを抜けてプログラムを終了

        # 空の入力をチェック
        if not ingredient_input.strip():
            continue # ループの最初に戻る

        # あいまい検索を実行
        result = fuzzy_convert_ingredient(ingredient_input, inci_jp_map, jp_inci_map)
        
        # 結果を表示
        print("\n--- 変換結果 ---")
        print(result)

# 3. エントリーポイントの定義
if __name__ == '__main__':
    main()


# In[ ]:




