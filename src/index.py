import io
import pandas
from flask import Flask, render_template, request
import re

app = Flask(__name__)


expected_columns = ['NOME', 'CARGO', 'E-MAIL', 'TELEFONE']


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		try:
			file = io.StringIO(request.files['file'].read().decode('utf-8'))
			df = pandas.read_csv(file)
			if len(set(expected_columns) & set(df.columns.values)) != 4:
				return render_template("index.html", error=True, type="COLUNAS INCORRETAS! COLUNAS ESPERADAS: NOME, CARGO, E-MAIL, TELEFONE")
			df["TELEFONE-LINK"] = df["TELEFONE"].apply(lambda x: '55' + re.sub(r'[^\d]', '', x))
			return render_template("output.html", pessoas=df.T.to_dict())
		except RuntimeError:
			return render_template("index.html", error=True, type="ERRO DESCONHECIDO")
		except pandas.errors.EmptyDataError:
			return render_template("index.html", error=True, type="ARQUIVO INVÁLIDO")
		except pandas.errors.ParserError:
			return render_template("index.html", error=True, type="ARQUIVO INVÁLIDO")
	else:
		return render_template("index.html")


if __name__ == "__main__":
	app.run(host="192.168.1.103",port=3000)
