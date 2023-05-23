import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from pacmap import PaCMAP
from umap import UMAP


df = pd.read_csv('../data/preprocessed/data.csv')
df.pop('country')

df_train = df[df.pop('year') == 2019]
gdp_pcap_log = df_train.pop('GDP.PCAP.LOG')


pca = PCA().fit(df_train)
x_pca = pca.transform(df_train)

plt.scatter(x_pca[:, 0], x_pca[:, 1], c=gdp_pcap_log, cmap='viridis')
plt.title('PCA')
plt.colorbar()
plt.savefig('visualization/pca.pdf', bbox_inches='tight')
plt.show()

plt.plot(pca.explained_variance_ratio_, marker='o', label='Variance ratio')
plt.plot(pca.explained_variance_ratio_.cumsum(), marker='o', color='red', linestyle='--', label='Cumulative variance')
plt.xlim(-0.5, 10.5)
plt.ylim(0, 1)
plt.legend()
plt.title('PCA explained variance')
plt.savefig('visualization/pca_variance.pdf', bbox_inches='tight')
plt.show()


x_umap = UMAP().fit_transform(df_train)
x_pacmap = PaCMAP().fit_transform(df_train)
x_tsne = TSNE().fit_transform(df_train)

plt.scatter(x_umap[:, 0], x_umap[:, 1], c=gdp_pcap_log, cmap='viridis')
plt.title('UMAP')
plt.colorbar()
plt.savefig('visualization/umap.pdf', bbox_inches='tight')
plt.show()

plt.scatter(x_pacmap[:, 0], x_pacmap[:, 1], c=gdp_pcap_log, cmap='viridis')
plt.title('PaCMAP')
plt.colorbar()
plt.savefig('visualization/pacmap.pdf', bbox_inches='tight')
plt.show()

plt.scatter(x_tsne[:, 0], x_tsne[:, 1], c=gdp_pcap_log, cmap='viridis')
plt.title('t-SNE')
plt.colorbar()
plt.savefig('visualization/tsne.pdf', bbox_inches='tight')
plt.show()
