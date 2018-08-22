"""

Aster : a kaggle bot to create baseline kernels for different category of kaggle competitions or datasets

__author__ == "shivam bansal"
__email__ == "shivam5992@gmail.com"

"""

import subprocess
import nbformat 
import json
import os

class Aster():

	## initialize the notebook parameters
	def __init__(self, config):
		self.nb = nbformat.v4.new_notebook()
		self.nb['cells'] = []
		self.config = config
		self.content_meta = "Meta/"
		self.kernel_meta = {"id": self.config["KERNEL_ID"], "title" : "Bot Generated Baseline Kernel", 
		"kernel_sources": [], "code_file": "baseline_kernel.ipynb", "language": "python", 
		"kernel_type": "notebook", "is_private": "false", "enable_gpu": "false", "enable_internet": "false"}

		## add the dataset sources 
		if self.config["DATASET"] != "":
			self.kernel_meta["dataset_sources"] = [self.config["DATASET"]]

		## add the competition sources
		if self.config["COMPETITION"] != "":
			self.kernel_meta["competition_sources"] = [self.config["COMPETITION"]]

		## create the folder for the kernel
		self.kernel_folder = "BaselineKernel"
		if not os.path.isdir(self.kernel_folder):
			os.makedirs(self.kernel_folder)

		## write the kernel-metadata.json
		fout = open(self.kernel_folder + "/kernel-metadata.json", "w")
		fout.write(json.dumps(self.kernel_meta))

	## function to prepare and modify the base content
	def _prepare_meta(self, filename):
		content = open(self.content_meta+filename).read()
		for key,value in self.config.items():
			if key.startswith("_"):
				content = content.replace("<"+key+">", value)
		return content

	## function to cleanup the content of the cell
	def _cleanup(self, string):
		string = string.replace("<text>","").replace("</text>","")
		string = string.replace("<code>","").replace("</code>","")
		string = string.replace("<num>","").replace("</doc>","")
		return string.strip()

	## function to check if a given cell is valid with respect to the config
	def is_valid_cell(self, line, flag):
		valid = True
		if line.startswith(flag+"<num>") and self.config["_TAG"] != "num":
			valid = False
		if line.startswith(flag+"<doc>") and self.config["_TAG"] != "doc":
			valid = False
		return valid

	## function to generate a new kernel
	def _prepare(self):
		for x in sorted(os.listdir(self.content_meta)):
			if x.startswith("."):
				continue

			txt = ""
			cod = ""
			content = self._prepare_meta(x)
			for j, line in enumerate(content.split("\n")):
				
				## add markdown cells
				if line.startswith("<text>"):
					txt = ""
				if line.startswith("</text>") and self.is_valid_cell(line, "</text>"):
					txt = self._cleanup(txt)
					self.nb['cells'].append(nbformat.v4.new_markdown_cell(txt))
					txt = ""
				txt += "\n"
				txt += line 

				## add code cells
				if line.startswith("<code>"):
					cod = ""
				if line.startswith("</code>") and self.is_valid_cell(line, "</code>"):
					cod = self._cleanup(cod)
					self.nb['cells'].append(nbformat.v4.new_code_cell(cod))
					cod = ""
				cod += "\n"
				cod += line 

		nbformat.write(self.nb, self.kernel_folder + "/baseline_kernel.ipynb")
		print ("Generated")
		return None 

	## function to push the generated kernel on kaggle
	def _push(self):
		command = "kaggle kernels push -p "+self.kernel_folder 
		subprocess.call(command.split())
		print ("Pushed")
		return None

## add default values 
config = {	"_TAG" : "num", 
			"_TEXT_COL" :  "text", 
		  	"_TARGET_COL" : "Outcome", 
		  	"_ID_COL" : "",

		  	"_TRAIN_FILE" : "diabetes", 
			"_TEST_FILE" : "",
		  	"COMPETITION" : "",
		  	"DATASET": "",
		  	"KERNEL_ID" : "shivamb/bot_generated_kernel",
		  	}
ast = Aster(config)
ast._prepare()
# ast._push()




### readme -- 29 onwards 
### adding defaults -- 29 onwards

### text kernel
### -- add some cool things 

### regression 
### -- add some cool things
















