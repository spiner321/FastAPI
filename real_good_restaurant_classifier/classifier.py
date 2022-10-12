# 텍스트를 분류하고 결과를 얻기 위한 함수

import torch
import torch.nn.functional as F

from transformers import BertTokenizerFast
from transformers import BertForSequenceClassification, AlbertForSequenceClassification

# config 객체에 분류할 text, 저장 경로 등 각종 정보를 담아 classify 함수를 호출하면 분류 결과를 얻을 수 있다.
def classify(config) -> list: # ->(화살표)는 함수 리턴값의 주석 역할
    saved_data = torch.load(config.model_fn,
                            map_location='cpu' if config.gpu_id < 0 else f'cuda:{config.gpud_id}')
    train_config = saved_data['config']
    bert_best = saved_data['bert']
    index_to_label = saved_data['classes']
    
    lines = config.lines
    
    with torch.no_grad():
        # Declare model and load pre-trained weights
        tokenizer = BertTokenizerFast.from_pretrained(train_config.pretrained_model_name)
        model_loader = AlbertForSequenceClassification if train_config.use_albert else BertForSequenceClassification
        model = model_loader.from_pretrained(train_config.pretrained_model_name,
                                             num_labels=len(index_to_label))
        
        model.load_state_dict(bert_best)

        if config.gpu_id >= 0:
            model.cuda(config.gpu_id)
        device = next(model.parameters()).device
        
        model.eval()

        y_hats = []
        for idx in range(0, len(lines), config.batch_size):
            mini_batch = tokenizer(lines[idx:idx + config.batch_size], 
                                   padding=True,
                                   truncation=True,
                                   return_tensors='pt',)
            
            x = mini_batch['input_ids']
            x = x.to(device)
            mask = mini_batch['attention_mask']
            mask = mask.to(device)
            
            # Take feed-forward
            y_hat = F.softmax(model(x, attention_mask=mask).logits, dim=-1)
            
            y_hats += [y_hat]
        
        # Concatenate the mini-batch wise result
        y_hats = torch.cat(y_hats, dim=0) # |y_hats| = (len(lines), n_classes)
        
        probs, indice = y_hats.cpu().topk(config.top_k) # |indice| = (len(lines), top_k)
        
        result = []
        for i, line in enumerate(lines):
            
            # clasification probability, 광고 여부, 분류한 텍스트를 담아 반환
            row = [float(probs[i][0]), index_to_label[int(indice[i][0])], line]
            result.append(row)
            
        return result