# clustering-practice-3H
クラスタリングの実験で使ったコード
青空文庫から小説をダウンロードして、品詞情報・tf-idfに基づいてk-meansをします。

授業で発表した概要・分析の結果: [./slide.pdf](./slide.pdf)

# データの準備
データの収集・前処理はPythonで行います。

環境はpipenvで管理しています。
- pipenv について https://qiita.com/y-tsutsu/items/54c10e0b2c6b565c887a
```
pip install pipenv
```
のようにして、pipenvをインストールした後、

```
pipenv install
```
を行えば、必要なパッケージのインストールが始まります。

その状態で、
```
pipenv shell
```
を実行すると、パッケージがインストールされた仮想環境に入ることができます。
Pythonスクリプトはすべて、この仮想環境内で動作する想定です。

`data-scripts`以下にデータを準備する用のスクリプトが置いてあります。
以下の順に実行すれば、`data`以下に、必要なデータが作成されます。
実際に分析に使うデータは、`pos_ratio_featured.tsv`と`tf_idf_featured.tsv`です。

1. `./data-scripts/scrape_books.py` - 青空文庫APIから`./author_list.txt`に書かれた作家の小説をダウンロードします。
2. `./data-scripts/normalize_data.py` - ダウンロードした小説から書式記号等を削除したり、文字数の少ない小説を省いたりします。
3. `./data-scripts/morphological_analyze.py` - 形態素解析して、結果を保存します。
4. `./data-scripts/make_vectorized_data.py` - 形態素解析の結果からデータを作ります。TF-IDFもここで行います。

# 解析コード
解析はRで行います。
`r-scripts`以下にデータを解析する用のスクリプトが置いてあります。
`./r-scripts/analyze_pos_featured.R`と`./r-scripts/analyze_tf_idf_featured.R`を実行すれば、クラスタリングが実行されます。