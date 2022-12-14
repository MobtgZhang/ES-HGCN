
import json
import os
import uuid
import sklearn
import pandas as pd
import numpy as np
import logging
from tqdm import tqdm
from bs4 import BeautifulSoup

logger = logging.getLogger()
from znlp.utils import split_content_labels

def split_aichallenger2018_dataset(data_dir,result_dir,tokenizer,train_per=0.75):
    train_file_name = os.path.join(data_dir,"sentiment_analysis_trainingset.csv")
    dev_file_name = os.path.join(data_dir,"sentiment_analysis_validationset.csv")
    id2label = ['location_traffic_convenience',
      'location_distance_from_business_district', 'location_easy_to_find',
      'service_wait_time', 'service_waiters_attitude',
      'service_parking_convenience', 'service_serving_speed', 'price_level',
      'price_cost_effective', 'price_discount', 'environment_decoration',
      'environment_noise', 'environment_space', 'environment_cleaness',
      'dish_portion', 'dish_taste', 'dish_look', 'dish_recommendation',
      'others_overall_experience', 'others_willing_to_consume_again']
    label2id = {word:idx for idx,word in enumerate(id2label)}
    save_data_dict = {
      "id2label":id2label,
      "label2id":label2id
    }
    save_dict_file = os.path.join(result_dir,"names-dict.json")
    with open(save_dict_file,mode="w",encoding="utf-8") as wfp:
        jline = json.dumps(save_data_dict)
        wfp.write(jline)
    dev_per = (1.0-train_per)/2
    test_per = dev_per
    train_dataset = pd.read_csv(train_file_name)
    dev_dataset = pd.read_csv(dev_file_name)
    all_dataset = pd.concat([train_dataset,dev_dataset])
    del train_dataset,dev_dataset
    all_dataset = sklearn.utils.shuffle(all_dataset)
    all_dataset[id2label] = all_dataset[id2label]+2
    
    train_len = int(train_per*len(all_dataset))
    dev_len = train_len + int(dev_per*len(all_dataset))
    
    train_dataset = all_dataset[:train_len]
    valid_dataset = all_dataset[train_len:dev_len]
    test_dataset = all_dataset[dev_len:]
    dataset_list = [train_dataset,valid_dataset,test_dataset]
    names_list = ['train','valid','test']
    for name,dataset in zip(names_list,dataset_list):
        id_dataset = dataset['id'].values.tolist()
        content_dataset = dataset['content'].values.tolist()
        labels_dataset = dataset[id2label].values.tolist()
        save_dataset_file = os.path.join(result_dir,"%sset.json"%name)
        split_content_labels(save_dataset_file,tokenizer,id_dataset,content_dataset,labels_dataset)
        logger.info("File saved in %s"%save_dataset_file)
def split_clueemotion2020_dataset(data_dir,result_dir,tokenizer):
    data_type_list = ['train','valid','test']
    id2label = ['like','happiness','sadness','anger','disgust','fear','surprise']
    label2id = {w:idx for idx,w in enumerate(id2label)}
    save_data_dict = {
      "id2label":id2label,
      "label2id":label2id
    }
    save_dict_file = os.path.join(result_dir,"names-dict.json")
    with open(save_dict_file,mode="w",encoding="utf-8") as wfp:
        jline = json.dumps(save_data_dict)
        wfp.write(jline)
    for data_type in data_type_list:
        load_txt_file = os.path.join(data_dir,"%s.txt"%data_type)
        save_json_file = os.path.join(result_dir,"%sset.json"%data_type)
        with open(load_txt_file,mode="r",encoding="utf-8") as rfp:
            with open(save_json_file,mode="w",encoding="utf-8") as wfp:
                for line in tqdm(rfp,desc="%s dataset process"%data_type):
                    data_dict = json.loads(line)
                    save_data_dict = {
                      "index":data_dict['id'],
                      "content":tokenizer.seg(data_dict['content']),
                      "labels":label2id[data_dict['label']]
                    }
                    jline = json.dumps(save_data_dict)
                    wfp.write(jline+"\n")
def split_wrime_dataset(data_dir,result_dir,tokenizer,version,name="Writer"):
    load_file_name = os.path.join(data_dir,version+".tsv")
    dataset = pd.read_csv(load_file_name,sep='\t')
    
    train_dataset = dataset[dataset['Train/Dev/Test']=='train'].drop(labels=['Train/Dev/Test'],axis=1).copy()
    valid_dataset = dataset[dataset['Train/Dev/Test']=='dev'].drop(labels=['Train/Dev/Test'],axis=1).copy()
    test_dataset = dataset[dataset['Train/Dev/Test']=='test'].drop(labels=['Train/Dev/Test'],axis=1).copy()
    del dataset
    data_list = [train_dataset,valid_dataset,test_dataset]
    names_list = ['train','valid','test']
    id2label = ['_Joy','_Sadness', '_Anticipation', '_Surprise','_Anger', '_Fear', '_Disgust', '_Trust']
    id2label = ["%s"%name+item for item in id2label]
    label2id = {word:idx for idx,word in enumerate(id2label)}
    save_data_dict = {
      "id2label":id2label,
      "label2id":label2id
    }
    save_dict_file = os.path.join(result_dir,"names-dict.json")
    with open(save_dict_file,mode="w",encoding="utf-8") as wfp:
        jline = json.dumps(save_data_dict)
        wfp.write(jline)
        
   
    for name,dataset in zip(names_list,data_list):
        id_dataset = dataset['UserID'].values.tolist()
        content_dataset = dataset['Sentence'].values.tolist()
        labels_dataset = dataset[id2label].values.tolist()
        save_dataset_file = os.path.join(result_dir,"%sset.json"%name)
        split_content_labels(save_dataset_file,tokenizer,id_dataset,content_dataset,labels_dataset)
        logger.info("File saved in %s"%save_dataset_file)
def split_carsreviews_dataset(data_dir,result_dir,tokenizer,train_per=0.7):
    load_file_name = os.path.join(data_dir,"train.csv")
    all_dataset = pd.read_csv(load_file_name)
    id2label = list(set(all_dataset["subject"]))
    label2id = {word:idx for idx,word in enumerate(id2label)}
    save_data_dict = {
        "id2label":id2label,
        "label2id":label2id
    }
    save_dict_file = os.path.join(result_dir,"names-dict.json")
    with open(save_dict_file,mode="w",encoding="utf-8") as wfp:
        jline = json.dumps(save_data_dict)
        wfp.write(jline)
    all_dataset = sklearn.utils.shuffle(all_dataset)
    length = len(all_dataset)
    categories = len(label2id)
    val_mat = np.ones(shape=(length,categories),dtype=np.int64)*(-2)
    for k in range(length):
        val_mat[k,label2id[all_dataset.loc[k,"subject"]]] = all_dataset.loc[k,"sentiment_value"]
    val_mat = val_mat + 2
    all_dataset[id2label] = val_mat
    all_dataset.drop(columns = ["subject","sentiment_value","sentiment_word"],inplace = True)
    dev_per = (1.0-train_per)/2.0
    train_len = int(train_per*len(all_dataset))
    dev_len = int((train_per+dev_per)*len(all_dataset))
    train_dataset = all_dataset.iloc[:train_len].copy()
    dev_dataset = all_dataset.iloc[train_len:dev_len].copy()
    test_dataset = all_dataset.iloc[dev_len:].copy()
    del all_dataset
    dataset_list = [train_dataset,dev_dataset,test_dataset]
    names_list = ['train','valid','test']
    
    for name,dataset in zip(names_list,dataset_list):
        id_dataset = dataset['content_id'].values.tolist()
        content_dataset = dataset['content'].values.tolist()
        labels_dataset = dataset[id2label].values.tolist()
        save_dataset_file = os.path.join(result_dir,"%sset.json"%name)
        split_content_labels(save_dataset_file,tokenizer,id_dataset,content_dataset,labels_dataset)
        logger.info("File saved in %s"%save_dataset_file)

def split_simplifyweibo4moods_dataset(data_dir,result_dir,tokenizer,train_per = 0.7):
    load_train_file = os.path.join(data_dir,'simplifyweibo_4_moods.csv')
    load_labels_file = os.path.join(data_dir,'labels.txt')
    all_dataset = pd.read_csv(load_train_file)
    label2id = []
    with open(load_labels_file,mode="r",encoding="utf-8") as rfp:
        for name in rfp:
            name = name.strip()
            label2id.append(name)
    id2label = {word:idx for idx,word in enumerate(label2id)}
    save_data_dict = {
        "id2label":id2label,
        "label2id":label2id
    }
    save_dict_file = os.path.join(result_dir,"names-dict.json")
    with open(save_dict_file,mode="w",encoding="utf-8") as wfp:
        jline = json.dumps(save_data_dict)
        wfp.write(jline)
    all_dataset = sklearn.utils.shuffle(all_dataset)
    dev_per = (1.0-train_per)/2.0
    train_len = int(train_per*len(all_dataset))
    dev_len = int((train_per+dev_per)*len(all_dataset))
    train_dataset = all_dataset.iloc[:train_len].copy()
    dev_dataset = all_dataset.iloc[train_len:dev_len].copy()
    test_dataset = all_dataset.iloc[dev_len:].copy()
    del all_dataset
    dataset_list = [train_dataset,dev_dataset,test_dataset]
    names_list = ['train','valid','test']
    for name,dataset in zip(names_list,dataset_list):
        id_dataset = [str(uuid.uuid1()).upper() for _ in range(len(dataset))]
        content_dataset = dataset["review"].values.tolist()
        labels_dataset = dataset["label"].values.tolist()
        save_dataset_file = os.path.join(result_dir,"%sset.json"%name)
        split_content_labels(save_dataset_file,tokenizer,id_dataset,content_dataset,labels_dataset)
        logger.info("File saved in %s"%save_dataset_file)
def split_toutiaonews_dataset(data_dir,result_dir,tokenizer,train_per = 0.7):
    load_all_file = os.path.join(data_dir,'toutiao_cat_data.txt')
    load_labels_file = os.path.join(data_dir,'labels.txt')
    all_dataset = []
    with open(load_all_file,mode="r",encoding="utf-8") as rfp:
        for line in rfp:
            value_list = line.split("_!_")
            ids = value_list[0]
            tag = value_list[2]
            sent = value_list[3]
            all_dataset.append([ids,tag,sent])
    # labels
    id2label = []
    with open(load_labels_file,mode="r",encoding="utf-8") as rfp:
        for line in rfp:
            vals_list = line.split()
            id2label.append(vals_list[-1])
    label2id = {word:idx for idx,word in enumerate(id2label)}
    save_data_dict = {
        "id2label":id2label,
        "label2id":label2id
    }
    save_dict_file = os.path.join(result_dir,"names-dict.json")
    with open(save_dict_file,mode="w",encoding="utf-8") as wfp:
        jline = json.dumps(save_data_dict)
        wfp.write(jline)
    all_dataset = sklearn.utils.shuffle(all_dataset)
    dev_per = (1.0-train_per)/2.0
    train_len = int(train_per*len(all_dataset))
    dev_len = int((train_per+dev_per)*len(all_dataset))
    all_dataset = pd.DataFrame(all_dataset,columns=["ids","label","review"])
    all_dataset = sklearn.utils.shuffle(all_dataset)
    dev_per = (1.0-train_per)/2.0
    train_len = int(train_per*len(all_dataset))
    dev_len = int((train_per+dev_per)*len(all_dataset))
    train_dataset = all_dataset.iloc[:train_len].copy()
    dev_dataset = all_dataset.iloc[train_len:dev_len].copy()
    test_dataset = all_dataset.iloc[dev_len:].copy()
    del all_dataset
    dataset_list = [train_dataset,dev_dataset,test_dataset]
    names_list = ['train','valid','test']
    for name,dataset in zip(names_list,dataset_list):
        id_dataset = dataset["ids"].values.tolist()
        content_dataset = dataset["review"].values.tolist()
        labels_dataset = dataset["label"].map(lambda x:label2id[x]).values.tolist()
        save_dataset_file = os.path.join(result_dir,"%sset.json"%name)
        split_content_labels(save_dataset_file,tokenizer,id_dataset,content_dataset,labels_dataset)
        logger.info("File saved in %s"%save_dataset_file)
def split_nlpcc2018task1_dataset(data_dir,result_dir,tokenizer):
    tag_dict = {"train":"train","dev":"valid"}
    id2label = ["Happiness","Sadness","Anger","Fear","Surprise"]
    label2id = { name:idx for idx,name in enumerate(id2label)}
    save_data_dict = {
        "id2label":id2label,
        "label2id":label2id
    }
    save_dict_file = os.path.join(result_dir,"names-dict.json")
    with open(save_dict_file,mode="w",encoding="utf-8") as wfp:
        jline = json.dumps(save_data_dict)
        wfp.write(jline)
    for tag_name in tag_dict:
        load_file = os.path.join(data_dir,'%s.txt'%tag_name)
        all_dataset = []
               
        with open(load_file,mode="r",encoding="utf-8") as rfp:
            bs = BeautifulSoup(rfp.read(),"lxml")
            for item in bs.find_all("tweet"):
                all_sentiments = {
                    "Happiness":item.happiness.text.strip(),
                    "Sadness":item.sadness.text.strip(),
                    "Anger":item.anger.text.strip(),
                    "Fear":item.fear.text.strip(),
                    "Surprise":item.surprise.text.strip()
                }
                for key in all_sentiments:
                    if all_sentiments[key].strip()=="T":
                        sentiment = key
                        break
                content = item.content.text.strip()
                val_list = [str(uuid.uuid1()).upper(),sentiment,content]
                all_dataset.append(val_list)
        all_dataset = pd.DataFrame(all_dataset,columns=["ids","label","review"])
        id_dataset = all_dataset["ids"].values.tolist()
        content_dataset = all_dataset["review"].values.tolist()
        labels_dataset = all_dataset["label"].map(lambda x:label2id[x]).values.tolist()
        save_dataset_file = os.path.join(result_dir,"%sset.json"%tag_dict[tag_name])
        split_content_labels(save_dataset_file,tokenizer,id_dataset,content_dataset,labels_dataset)
        logger.info("File saved in %s"%save_dataset_file)

          