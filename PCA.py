import numpy.linalg as ln
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


################################
# Principal Component Analysis #
################################


# Scaling  
mean = np.mean(df, axis=0)
sdt = np.std(df, axis=0)
# normalized df
dfn = (df - mean)/sdt

# Correlation matrix
Csc = np.dot(dfn.T, dfn)*1/dfn.shape[0]

# eigenvalues
d, P = ln.eig(Csc)
idx = abs(d).argsort()[::-1]
d = d[idx]
# Eigenvectors matrix
P = P[:, idx]
# Eigenvalues matrix
D = np.diag(d)

# Inertia
pct_inertia = np.zeros(7)
for i in range(len(d)):
    pct_inertia[i] = (d[i]/sum(d)*100)
inertia = np.cumsum(pct_inertia)

# inertia diagram, scree diagram
label_axe = ['PC'+str(i+1) for i in range(pct_inertia.shape[0])]
plt.figure(figsize=(10, 4))
plt.bar(range(pct_inertia.shape[0]), pct_inertia, color='#2b9093')
plt.title('Inertia per axis')
plt.xticks(range(pct_inertia.shape[0]), label_axe)
plt.ylabel('%Inertia ')
plt.xticks(rotation=90)
plt.plot(d*10, color='black') #*10 so the eigen values are more visible. Do not read eig from plot
l1 = mpt.Patch(color='black', label='10*eigen values')
plt.legend(handles=[l1])
plt.tight_layout()
plt.show()

# new basis: Xn.P
dfnew = pd. DataFrame(np.dot(dfn, P))
newvar = ['PC'+str(i+1) for i in range(0, P.shape[0])]
dfnew.columns = newvar

# scatter plot
plt.scatter(dfnew['PC1'], dfnew['PC2'], edgecolor = 'k')
plt.title('PC1 and PC2 in new base', size=8)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.tight_layout()
plt.show()


######################
#Variable Factor Map #
######################


plt.style.use('ggplot')  # Load the data
scaler = StandardScaler()
scaler.fit(df.iloc[:,1:])
df2 = scaler.transform(df.iloc[:,1:])  # The PCA model
pca = PCA()  # estimate only 2 PCs

# project the original data into the PCA space
df2_new = pca.fit_transform(df2)

# Plot 
(fig, ax) = plt.subplots(figsize=(12, 12))
for i in range(0, len(pca.components_)):
    ax.arrow(0, 0,
              pca.components_[0, i], pca.components_[1, i],
              head_width=0.05, head_length=0.05, color='red')
    plt.text(pca.components_[0, i] + 0.05,
             pca.components_[1, i] + 0.05, df.iloc[:,1:].columns.values[i])

an = np.linspace(0, 2 * np.pi, 100)
plt.plot(np.cos(an), np.sin(an))
plt.axis('equal')
ax.set_title('Variable factor map')
plt.show()
