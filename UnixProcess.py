import os
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
import numpy as np


def plot_unix(n, r, path_rel, path_abs, file_name, nr):
	"""
	Generates and saves the curves automatically
	"""
	with open(os.path.join(path_abs, file_name), "r") as file:
		labels = [int(i.strip()) for i in file.read().split('\n') if len(i) > 0]

	cmd = f"java -jar negsel2.jar -alphabet file://{path_rel}{file_name[:-9]}.alpha -self {path_rel}{file_name[:-9]}.train \
		-n {n} -r {r} -c -l < {path_rel}{file_name[:-9]}.{nr}.test"
	output = os.popen(f"{cd} && {cmd}").read()
	scores_per_sequence = output.split('\n')[:-1]  # slice to get rid of last empty line

	means = []
	for s in scores_per_sequence:
		scores = [float(i) for i in s.split(' ') if len(i) > 0]
		means.append(np.mean(scores))

	print(len(means))
	print(means)
	auc_score = roc_auc_score(labels, means)
	fpr, tpr, _ = roc_curve(labels, means)
	fig = plt.figure()
	plt.plot(fpr, tpr)
	plt.plot([0, 1], [0, 1], linestyle='dashed')
	plt.title(f"AUC Curve; r={r}, AUC Score = {round(auc_score, 2)}, file: {file_name[:-7]}.test")
	plt.grid(zorder=-1)
	plt.xlabel("1-specificity")
	plt.ylabel("sensitivity")
	if not os.path.isdir("img2"):
		os.mkdir("img2")
	plt.savefig(f"img2\\Unix_curves_r_{r}_{file_name[:-7]}.png")
	print("Done")


if __name__ == '__main__':
	# beware of \" for folders with spaces in it
	cd = 'cd C:\\Users\\sboos\\"Google Drive"\\UNI\\"Natural Computing"\\A2\\negative-selection'
	prefix = "syscalls\\"

	nr = 1  # to switch which file to use for testing, change the nr variable
	folder1 = 'snd-cert'
	folder2 = 'snd-unm'

	folder_path = f"{prefix}{folder1}\\"
	folder_path2 = f"{prefix}{folder2}\\"
	file_name = f"{folder1}.{nr}.labels"
	file_name2 = f"{folder2}.{nr}.labels"

	# these paths are not allowed to have \"  in them despite having spaces in folder names
	path = f"C:\\Users\\sboos\\Google Drive\\UNI\\Natural Computing\\A2\\negative-selection\\{folder_path}"
	path2 = f"C:\\Users\\sboos\\Google Drive\\UNI\\Natural Computing\\A2\\negative-selection\\{folder_path2}"
	n = 7
	r = 7

	for r_ in range(1, r+1):
		plot_unix(n, r_, folder_path, path, file_name, nr=nr)  # cert folder
		plot_unix(n, r_, folder_path2, path2, file_name2, nr=nr)  # unm folder

