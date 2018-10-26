import matplotlib
import matplotlib.pyplot as plt
x = [1,2,3,4,5]
y = [3/10,3/10,0/10,1/10,2/10]
plt.xticks([0,1,2,3,4,5])
plt.plot(x,y,'-o')
plt.xlabel('Querie')
plt.ylabel('Precision')
plt.show()