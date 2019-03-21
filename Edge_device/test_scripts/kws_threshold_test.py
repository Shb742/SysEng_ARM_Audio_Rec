import matplotlib.pyplot as plt
import numpy as np
import tester
#"help me /1e-22/"
keyphrase_list = []

def load_kps():
	global keyphrase_list
	with open("keyphrase_list") as kps_file:
		for line in kps_file:
			keyphrase_list.append(line)

def update_kps(index,threshold,threshold_factor=1):
	global keyphrase_list
	keyphrase_list[index] = keyphrase_list[index].split("/",1)[0]+"/"+str(threshold_factor)+"e-"+str(threshold)+"/\n"
	print(keyphrase_list[index])
	kps_list = open("keyphrase_list","w")
	kps_list.write(keyphrase_list[index])
	kps_list.close()

def get_data(index,lower_bound,upper_bound,threshold_factor_lower=1,threshold_factor_upper=1,tf_step=1):
	tpr_points = []
	fpr_points = []
	ppv_points = []
	load_kps()
	upper_bound+=1
	threshold_factor_upper+=tf_step
	for i in range(upper_bound-lower_bound):
		for j in range( (threshold_factor_upper - threshold_factor_lower)//tf_step ):
			update_kps(index,lower_bound+i,j*tf_step+threshold_factor_lower)
			f,t,p = tester.test()
			tpr_points.append(t)
			fpr_points.append(f)
			ppv_points.append(p)
			print("Total_Progress ="+str((i*100.0/(upper_bound-lower_bound)))+"%")
	return (tpr_points,fpr_points,ppv_points)

#Get values
tpr_points, fpr_points,ppv_points = get_data(0,0,30)
kps_list = open("keyphrase_list","w")
kps_list.write("".join(keyphrase_list))
kps_list.close()

print(tpr_points)
print(fpr_points)
print (ppv_points)
# This is the AUC
auc = abs(np.trapz(tpr_points,fpr_points))
print("Area Under Curve - "+str(auc))


title = "keyword threshold"
plt.figure(title)
# This is the ROC curve
plt.subplot(211)
plt.title("ROC curve")
plt.xlim([-0.01, 1.02])
plt.ylim([-0.01, 1.2])
#Plot no skill
plt.plot([0, 1], [0, 1], linestyle='--')
plt.plot(fpr_points,tpr_points,'r-.')
plt.ylabel("True positive rate")
plt.xlabel("False positive rate")
#plt.gca().invert_xaxis()#inver x axis so it makes sense

plt.subplot(212)
plt.title("PRC curve")
plt.xlim([-0.01, 1.02])
plt.ylim([-0.01, 1.02])
# plot no skill
plt.plot([0, 1], [0.5, 0.5], linestyle='--')
plt.plot(tpr_points,ppv_points,'r-.')
plt.ylabel("Positive predictive value")
plt.xlabel("True positive rate")


plt.show() 