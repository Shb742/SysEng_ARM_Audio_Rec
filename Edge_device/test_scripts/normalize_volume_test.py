import matplotlib.pyplot as plt
import numpy as np
import tester


def get_data(x_min,x_max,x_step):
	tpr_points = []
	fpr_points = []
	ppv_points = []
	for i in range(((x_max-x_min)//x_step)):
		f,t,p = tester.test(x_min+(x_step*i))
		tpr_points.append(t)
		fpr_points.append(f)
		ppv_points.append(p)
		print("Total_Progress ="+str((i*1.0/((x_max-x_min)//x_step))))
	return (tpr_points,fpr_points,ppv_points)

#Get values
tpr_points, fpr_points,ppv_points = get_data(1,25,1)

print(tpr_points)
print(fpr_points)
print (ppv_points)
# This is the AUC
auc = abs(np.trapz(tpr_points,fpr_points))
print("Area Under Curve - "+str(auc))


title = "test_normalize_volume"
plt.figure(title)
# This is the ROC curve
plt.subplot(211)
plt.title("ROC curve")
plt.xlim([0, 1])
plt.ylim([0, 1])
#Plot no skill
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr_points,tpr_points,'r-.')
plt.ylabel("True positive rate")
plt.xlabel("False positive rate")
#plt.gca().invert_xaxis()#inver x axis so it makes sense

plt.subplot(212)
plt.title("PRC curve")
plt.xlim([0, 1])
plt.ylim([0, 1])
# plot no skill
plt.plot([0, 1], [0.5, 0.5], linestyle='--')
plt.plot(tpr_points,ppv_points,'r-.')
plt.ylabel("Positive predictive value")
plt.xlabel("True positive rate")


plt.show() 