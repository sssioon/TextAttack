from textattack.shared import utils
import torch

from textattack.tokenizers import BERTTokenizer, BERTEntailmentTokenizer
from transformers.modeling_bert import BertForSequenceClassification


class BERTForClassification:
    """ 
    BERT fine-tuned for textual classification. 

    Args:
        model_path(:obj:`string`): Path to the pre-trained model.
        num_labels(:obj:`int`, optional):  Number of class labels for 
            prediction, if different than 2.
            
    """
    def __init__(self, model_path, num_labels=2, entailment=False):
        #model_file_path = utils.download_if_needed(model_path)
        model_file_path = utils.download_if_needed(model_path)
        # model_file_path = '/p/qdata/jm8wx/research/text_attacks/RobustNLP/BertClassifier/outputs-counterfit/mr-uncased-2020-03-05-11:21/checkpoint-54600/'
        self.model = BertForSequenceClassification.from_pretrained(
            model_file_path, num_labels=num_labels)
        self.model.to(utils.get_device())
        self.model.eval()
        if entailment:
            self.tokenizer = BERTEntailmentTokenizer()
        else:
            self.tokenizer = BERTTokenizer(model_file_path, fast=False)
    
    def __call__(self, *params):
        pred = self.model(*params)[0]
        return torch.nn.functional.softmax(pred, dim=-1)
