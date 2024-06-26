import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
cm = 1/2.54
fig, ax = plt.subplots(figsize=[8.3*cm,8.3*cm/(golden_ratio)], dpi=300)

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#array to store wake efficiencies
eta_w = np.zeros(40)
#array to store mean yaw angles
mean_yaw = np.zeros(40)

for i in range(40):
    eta_w[i] = loss_factors[i][1]
    mean_yaw[i] = loss_factors[i][11]

#exclude cases H300-C0-G0 and H150-C0-G0
index_mask = [i != 20 and i != 30 for i in range(40)]
plt.scatter(mean_yaw[index_mask], eta_w[index_mask], c='b', marker='x')

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(mean_yaw[index_mask].reshape(-1, 1), eta_w[index_mask].reshape(-1, 1))

#calculate r2 score
y_predict = regr.predict(mean_yaw[index_mask].reshape(-1, 1))
r_squared = r2_score(eta_w[index_mask], y_predict)
plt.text(1,1.2, rf'$R^2={round(r_squared,3)}$', ha='left', va='top')

#plot linear regression
x = np.linspace(0.75,4)
y = regr.predict(x.reshape(-1, 1))
plt.plot(x,y,c='k')

#plt.xlim([0,1.1])
#plt.ylim([0,1.4])

plt.tight_layout()
plt.ylabel(r'$\eta_{w}$ [-]')
plt.xlabel(r'$\overline{|\Phi|}$ [deg.]')
plt.savefig('KirbyFig1a.png', bbox_inches='tight')
plt.savefig('fig1a.pdf', bbox_inches='tight')
