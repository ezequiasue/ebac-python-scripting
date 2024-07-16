import csv
import sys
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Verifique se o argumento foi fornecido
if len(sys.argv) < 2:
    print("Uso: python visualizacao.py <output_filename>")
    sys.exit(1)

# Carregar o argumento
output_filename = sys.argv[1]

# Extraindo as colunas hora e taxa
df = pd.read_csv('./taxa-cdi.csv')

# Verifique os valores únicos antes da conversão
print("Valores únicos na coluna 'hora' antes da conversão:", df['hora'].unique())

# Limpe os dados: remova ou corrija valores que não correspondem ao formato esperado
df = df[df['hora'].str.match(r'^\d{2}:\d{2}:\d{2}$')]

# Convertendo a coluna 'hora' para datetime
df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S', errors='coerce')

# Remova valores nulos após a conversão
df = df.dropna(subset=['hora'])

# Verifique os valores únicos após a limpeza e conversão
print("Valores únicos na coluna 'hora' após a conversão:", df['hora'].unique())

# Criando um gráfico mais interessante: scatter plot com linha de tendência
plt.figure(figsize=(12, 8))
grafico = sns.scatterplot(x=df['hora'], y=df['taxa'], hue=df['taxa'], palette='coolwarm', size=df['taxa'], sizes=(20, 200), legend=None)
sns.lineplot(x=df['hora'], y=df['taxa'], color='blue', errorbar=None)

# Definindo os ticks e os rótulos corretamente
grafico.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
grafico.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

# Melhorar a apresentação do gráfico
plt.title('Taxa CDI ao Longo do Tempo')
plt.xlabel('Hora')
plt.ylabel('Taxa')
plt.xticks(rotation=45)
plt.grid(True)

# Salvando o gráfico
plt.tight_layout()
grafico.get_figure().savefig(f"{output_filename}.png")

print(f"Gráfico salvo como {output_filename}.png")
