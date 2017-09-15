from pymongo import MongoClient
import gridfs
import os

def hide_encrypted_file(db_name,file_name,enc_type,password,destruct_number=None) :

	client = MongoClient()
	db=client[db_name]
	file_input= gridfs.GridFS(db)
	slash_index=file_name.rfind("/")
	dot_index=file_name.rfind(".")
	source_file=file_name[slash_index+1:dot_index]
	data=open(file_name,"rb").read()
	id=file_input.put(data,filename=file_name)


	db.hidden_files.insert_one({"file_id":id,"filename":source_file,"encrptiontype":enc_type,"password":password,"destruct":destruct_number})
	os.remove(file_name)

def unhide_encrypted_file(db_name,file_name,password,target_folder):
	client=MongoClient()
	db=client[db_name]
	hidden=db.hidden_files
	files=db.fs.files
	fs=gridfs.GridFS(db)
	ref_file=hidden.find_one({"filename":file_name},{"_id":0,"file_id":1,"filename":1,"destruct":1,"password":1})
	destruct=int(ref_file['destruct'])
	print destruct
	orig_password=ref_file['password']
	if password!=str(orig_password):
		destruct=destruct -1
		hidden.update_one({"filename":file_name},{"$set":{"destruct":str(destruct)}})
	if password==str(orig_password):
		data=fs.get(ref_file['file_id']).read()
		target=target_folder+"/"+ref_file['filename']
		file=open(target+".enc","wb")
		file.write(data)
		hidden.remove({"filename":file_name})
		files.remove({"_id":ref_file['file_id']})
	if destruct==0:
		hidden.remove({"filename":file_name})
		files.remove({"_id":ref_file['file_id']})
	return destruct

def show_files(db_name):
	client=MongoClient()
	db=client[db_name]
	hidden=db.hidden_files
	all_files=hidden.find({})
	print "FILENAME       "+"DATE    "+"   TIME "
	print "\n"
	for doc in all_files:
		print  str(doc['filename']) +" "+ str(doc['_id'].generation_time)
		print "\n"


def update_history(db_name,content):
	client=MongoClient()
	db=client[db_name]
	history=db.history
	history.insert_one({"content":content})


def db_activate(db_name):
	client=MongoClient()
	db=client[db_name]
	sample=db.sample
	sample.insert_one({"sample":"sample"})
