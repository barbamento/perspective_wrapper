import os
import pandas as pd
from perspective import PerspectiveAPI
from typing import List
import numpy as np

def create_directories(dir: str, parent: bool = False):
    if parent:
        if not os.path.exists(dir):
            for i in [
                "/".join(dir.split("/")[:j]) for j in range(1, len(dir.split("/")) + 1)
            ]:
                create_directories(i)
    else:
        if not os.path.exists(dir):
            os.mkdir(dir)

class key:
    path="key/perspective.csv"

    def __init__(self):
        if not os.path.exists(self.path):
            pd.DataFrame(columns=["owner","key","n_call"]).to_csv(self.path,index=False)
        self.key_df=pd.read_csv(self.path,index_col="owner")
        print(self.key_df)
        user=input("who is the key owner?")
        if self.key_df.empty or not user in self.key_df.index:
            self.create_user(user)
        self.key=self.key_df.loc[user,"key"]
        self.n_call=self.key_df.loc[user,"n_call"]
        print(self.key,self.n_call)

    def create_user(self,user:str):
        self.key_df.loc[user,:]=[
            input("write the perspective labeller key"),
            input("how many call per second do you have?")
        ]
        self.key_df.to_csv(self.path,index="owner")


def split_in(path: str, n: int, name: str):
    df = pd.read_csv(path)
    list_df: List[pd.DataFrame] = np.array_split(df, n)
    for i in range(len(list_df)):
        list_df[i].to_csv(f"{name}_{i}.csv")


def label(col_id:str,col_text:str,data_path:str="dataset",delete_tmp:bool=True):
    """
    function created to label csv (or ndjson) of data.
    it requires a path inside of which csv are stored.

    arguments:

        col_id : str
    the name of the column of the comment ids

        text_id : str
    the name of the column of the comment text

        data_path : str = "dataset"
    the path of the folder in which the data are stored

        delete_tmp:bool = True
    if False keep the temporary dataset used to speed up and ease the labelling process.
    otherwise it deletes them after the labelling process
    """
    create_directories("labelled_tmp",parent=True)
    create_directories("results",parent=True)
    k=key()
    for f in os.listdir(data_path):
        path=f"{data_path}/{f}"
        if path.endswith(".csv"):
            try:
                non_labelled_df = pd.read_csv(
                    path,
                    lineterminator="\n",
                    dtype={"id": "string", "conversation_id": "string"},
                )
            except:
                non_labelled_df = pd.read_csv(
                    path,
                    encoding="latin-1",
                    lineterminator="\n",
                    dtype={"id": "string", "conversation_id": "string"},
                )
            print(non_labelled_df.columns)
        elif path.endswith(".ndjson"):
            non_labelled_df = pd.read_json(
                path,
                lines=True,
            )
        else:
            raise ValueError(f"error in {path}")
        non_labelled_df = non_labelled_df[non_labelled_df[col_text].notna()]



if __name__=="__main__":
    key()
    