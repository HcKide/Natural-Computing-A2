import os
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.metrics import roc_curve, roc_auc_score


def generate_auc_curve(max_r, cd, test_file, language="tagalog"):
	"""
	Generates and saves the curves automatically
	"""
	outputs = {}

	for r in tqdm(range(1, max_r+1)):
		cmd_eng = f"java -jar negsel2.jar -self english.train -n 10 -r {r} -c -l < english.test"
		cmd_anomaly = f"java -jar negsel2.jar -self english.train -n 10 -r {r} -c -l < {test_file}"
		out_eng = os.popen(f"{cd} && {cmd_eng}").read()
		out_tag = os.popen(f"{cd} && {cmd_anomaly}").read()

		eng = [(float(i.strip()), 0) for i in out_eng.split('\n') if len(i) > 0]
		anomaly = [(float(i.strip()), 1) for i in out_tag.split('\n') if len(i) > 0]

		outputs[r] = eng + anomaly
		outputs[r] = sorted(outputs[r], key=lambda x: x[0])

	for r in outputs.keys():
		y_true = [label for value, label in outputs[r]]
		y_scores = [value for value, label in outputs[r]]
		auc_score = roc_auc_score(y_true, y_scores)
		fpr, tpr, _ = roc_curve(y_true, y_scores)
		fig = plt.figure()
		plt.plot(fpr, tpr)
		plt.plot([0, 1], [0, 1], linestyle='dashed')
		plt.title(f"AUC Curve with r={r} and AUC Score: {round(auc_score, 2)}, english vs. {language}")
		plt.grid(zorder=-1)
		plt.xlabel("1-specificity")
		plt.ylabel("sensitivity")
		if not os.path.isdir("img"):
			os.mkdir("img")
		plt.savefig(f"img\\AUC_Curve_r{r}_eng_vs_{language[:4]}.png")
	print(f"\nDone with {language}\n")


if __name__ == '__main__':
	## put the directory here where the negative-selection folder is saved, use \" for folders with spaces in the name
	cd = 'cd C:\\Users\\sboos\\"Google Drive"\\UNI\\"Natural Computing"\\A2\\negative-selection'
	max_r = 9
	lang_folder = "lang\\"

	test_file_tag = "tagalog.test"
	test_file_hili = f"{lang_folder}hiligaynon.txt"
	test_file_middle_eng = f"{lang_folder}middle-english.txt"
	test_file_plautdietsch = f"{lang_folder}plautdietsch.txt"
	test_file_xhosa = f"{lang_folder}xhosa.txt"

	generate_auc_curve(max_r, cd, test_file_tag, language="tagalog")
	# generate_auc_curve(max_r, cd, test_file_hili, language="hiligaynon")
	# generate_auc_curve(max_r, cd, test_file_middle_eng, language="middle-english")
	# generate_auc_curve(max_r, cd, test_file_plautdietsch, language="plautdietsch")
	# generate_auc_curve(max_r, cd, test_file_xhosa, language="xhosa")
